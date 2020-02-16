# frozen_string_literal: true

module Api
  module V1
    class SchoolsController < BaseApiController
      before_action :authenticate_user_from_token!
      before_action :authentication_error,
                    if: :guest_user?,
                    except: %i[pick search_school]
      UNIVERSITY_AGE = 17
      swagger_controller :schools, 'School Management'

      def self.add_common_params(api)
        api.param :header, 'uid', :string, :required, 'conects id'
        api.param :header, 'access-token', :string, :required, 'Authentication token'
        api.param :header, 'token-type', :string, :required, 'Bearer'
      end

      def self.add_common_response(api)
        api.response :forbidden
        api.response :not_found
        api.response :not_acceptable
      end

      swagger_api :pick do |api|
        summary '추천 학교 리스트'
        Api::V1::BoardsController.add_common_params(api)
        param :query, 'page', :integer, :required, 'page'
        param :query, 'per_page', :integer, :required, 'per_page'
        Api::V1::BoardsController.add_common_response(api)
      end

      swagger_api :search_school do |api|
        summary '학교 검색에 대한 학교 리스트 리턴'
        Api::V1::BoardsController.add_common_params(api)
        param :query, :keyword, :string, :required, '학교 검색 키워드'
        param :query, :page, :integer, :optional, 'page'
        param :query, :per_page, :integer, :optional, 'per_page'
        Api::V1::BoardsController.add_common_response(api)
      end

      def pick
        picked_schools = current_user.present? ? current_user_pick : guest_pick
        schools_json = {
          my_school: my_school,
          picked_schools: []
        }
        if picked_schools.present?
          picked_schools.each do |school|
            schools_json[:picked_schools].push(
              school_id: school['id'],
              type_cd: school['code_key'],
              school_name: school['school_name'],
              thumbnail: school['thumbnail'],
              locale: school['locale']
            )
          end
        end
        render json: { result: schools_json, meta: get_page_info(picked_schools) }
      end

      def search_school
        keyword = if params[:keyword].present?
                    params[:keyword].strip.downcase
                  else
                    ''
                  end
        page = params[:page].present? ? params[:page].to_i : 1
        per_page = params[:per_page].present? ? params[:per_page].to_i : 10
        if keyword.present?
          searched_schools = StudySchool.where('lower(school_name) LIKE ?', '%' + keyword + '%').where(locale: current_user.locale).page(page).per(per_page)
        else
          searched_schools = StudySchool.where(school_name: '').where(locale: current_user.locale)
        end
        searched_schools = searched_schools.page(page).per(per_page)
        schools_json = []
        if searched_schools.present?
          searched_schools.each do |school|
            schools_json.push(
              school_id: school.id,
              type_cd: school.code_key,
              school_name: school.school_name,
              thumbnail: school.thumbnail
            )
          end
        end
        render json: { result: schools_json, meta: get_page_info(searched_schools) }
      end

      private

      def current_user_pick
        @page = params[:page].present? ? params[:page].to_i : 1
        @per_page = params[:per_page].present? ? params[:per_page].to_i : 10
        # picked_schools = StudySchool.where(code_key: school_level, pick: true, locale: current_user.locale).page(page).per(per_page)
        picked_schools = fetch_picked_schools
        picked_schools
      end

      def my_school
        my_school = nil
        if current_user.selected_school.present?
          school = current_user.selected_school.study_school.presence
          if school.present?
            my_school = {
              school_id: school.id,
              type_cd: school.code_key,
              school_name: school.school_name,
              thumbnail: school.thumbnail,
              locale: school.locale
            }
          end
        end
        my_school
      end

      def guest_pick
        # 가회원인 경우 보여줄 추천 리스트, 추후 작업 예정
      end

      def fetch_picked_schools
        year_of_birth = current_user.year_of_birth.presence || 17
        school_level = school_level(year_of_birth)
        picked_schools_redis_key = "v1_schools_pick_#{school_level}_#{current_user.locale}"
        picked_schools_redis = Redis.current.get(picked_schools_redis_key)
        if picked_schools_redis.present? && valid_json?(picked_schools_redis)
          picked_schools = Kaminari.paginate_array(JSON.parse(picked_schools_redis)).page(@page).per(@per_page)
        else
          picked_schools = StudySchool.where(code_key: school_level, pick: true, locale: current_user.locale)
          Redis.current.set("v1_schools_pick_#{school_level}_#{current_user.locale}", picked_schools.to_json, ex: 86_400)
          picked_schools = Kaminari.paginate_array(picked_schools.to_a).page(@page).per(@per_page)
        end
        picked_schools
      end

      def school_level(year_of_birth) # 나이에 따른 초/중/고/대학교 계산
        current_year = DateTime.current.year
        if current_year - year_of_birth >= UNIVERSITY_AGE
          return 'SCTP004'
        else
          return 'SCTP003'
        end
      end
    end
  end
end