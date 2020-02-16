# -*- coding: utf-8 -*- 
from config import env
from controller import diffs_controller
import glob
import os.path
import sys

class DiffPy:
    def __init__(self, old=' ', new=' '):
        self.__old = old.strip()
        self.__new = new.strip()
        self.__check_file_name()

    def diff(self):
        diffs_controller.DiffsController(self.__old, self.__new)

    def __check_file_name(self):
        self.__check_number_of_args()
        self.__check_file_format()
        self.__check_file_name_same()
        self.__check_file_name_exist()
        
    ## Exception1: Check the Numbers of Args when initializing
    def __check_number_of_args(self):
        try:
            if self.__old == '' or self.__new == '':
                raise Exception('파일명을 두 가지 모두 입력해서 diffpy class로부터 object를 생성해주세요.')
        except Exception as e:
            print(env.BasicErrorMessage, e), sys.exit(1)

    ## Exception2: Check if the File Name has Extension type
    def __check_file_format(self):
        try:
            available_ext = env.ext
            if not (len(self.__old)>=3 and self.__old.endswith(available_ext)):
                raise Exception('좌측 old 파일 이름은 지원되지 않는 확장자입니다. 파일명의 확장자를 확인해서 입력해주세요.')
            elif not (len(self.__new)>=3 and self.__new.endswith(available_ext)):
                raise Exception('우측 new 파일 이름은 지원되지 않는 확장자입니다. 파일명의 확장자를 확인해서 입력해주세요.')
            else:
                pass
        except Exception as e:
            print(env.BasicErrorMessage, e), sys.exit(1)

    ## Exception3: Check if both old and new file name are different each other.

    def __check_file_name_same(self):
        try:
            if self.__old == self.__new:
                raise Exception('좌측 old 와 우측 new 파일은 서로 달라야 합니다.')
        except Exception as e:
            print(env.BasicErrorMessage, e), sys.exit(1)
        
    ## Exception4: Not Found FileName in the 'text' Folder
    def __check_file_name_exist(self):
        try:
            if self.__find_file_name(self.__old) == False:
                raise Exception('좌측 old 파일 이름을 경로에서 찾을 수 없습니다. 파일 이름을 다시 확인해주세요.')
            elif self.__find_file_name(self.__new) == False:
                raise Exception('우측 new 파일 이름을 경로에서 찾을 수 없습니다. 파일 이름을 다시 확인해주세요.')
            else:
                pass
        except Exception as e:
            print(env.BasicErrorMessage, e), sys.exit(1)

    def __find_file_name(self, file_name):
        file_list = glob.glob('./text/*'+os.path.splitext(file_name)[-1])
        for item in file_list:
            if os.path.basename(item) == file_name:
                return True
        return False 

    