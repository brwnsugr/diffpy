class DiffsController:

    def __init__(self, old=None, new=None):
        self.__old_text = self.__text_process(old)
        self.__new_text = self.__text_process(new)
        self.__compare_files()
         
    def __text_process(self, file):
        f = open('./text/'+file, 'r')
        lines = f.readlines()
        return lines

    def __compare_files(self):
        common_string_list = self.__longest_common_subsequence()
        self.__diff_calculate(common_string_list)
        
    def __longest_common_subsequence(self):
        old_lines = sum(1 for line in self.__old_text)
        new_lines = sum(1 for line in self.__new_text)
        LCS = [[0]*(old_lines+1) for i in range(new_lines+1)]
        ans = 0
        for i in range(1, new_lines + 1):
            for j in range(1, old_lines + 1):
                if self.__new_text[i - 1] == self.__old_text[j - 1]:
                    LCS[i][j] = LCS[i-1][j-1] + 1
                else:
                    LCS[i][j] = max([LCS[i][j-1], LCS[i-1][j]])

        i = new_lines
        j = old_lines
        common_string_list = []
        while i != 0 and j != 0:
            if LCS[i - 1][j] < LCS[i][j] and LCS[i][j - 1] < LCS[i][j]:
                common_string_list.append(self.__new_text[i-1])
                i -= 1
                j -= 1
            elif LCS[i - 1][j] < LCS[i][j]:
                j -= 1
            elif LCS[i][j - 1] < LCS[i][j]:
                i -= 1
            else:  
                i -= 1
                j -= 1
        common_string_list.reverse()
        return common_string_list
    
    def __diff_calculate(self, list):
        old_lines = sum(1 for line in self.__old_text)
        new_lines = sum(1 for line in self.__new_text)
        old_pairs = []
        new_pairs = []
        old_pairs = self.__line_order(list,self.__old_text)
        new_pairs = self.__line_order(list,self.__new_text)
        answer= []
        tmp = 0
        tmp2 = 0
        for idx, val in enumerate(list):
            while tmp2 < len(new_pairs):
                if new_pairs[tmp2][0] == idx:
                    answer.append("+ " + new_pairs[tmp2][1])
                    tmp2 += 1
                elif new_pairs[tmp][0] >= len(list):
                    answer.append("+ "+new_pairs[tmp2][1])
                    tmp2 += 1
                else:
                    break

            while tmp < len(old_pairs):
                if old_pairs[tmp][0] == idx:
                    answer.append("- " + old_pairs[tmp][1])
                    tmp += 1
                elif old_pairs[tmp][0] >= len(list):
                    answer.append("- "+old_pairs[tmp][1])
                    tmp += 1
                else:
                    break
            answer.append(val)
        for item in answer:
            print(item)

        

 
    def __line_order(self, common_list, text_list):
        pairs = []
        tmp = 0  
        for common_idx, common_val in enumerate(common_list):
            while tmp < len(text_list):
                if text_list[tmp] != common_val:
                    pairs.append((common_idx, text_list[tmp]))
                    tmp+=1
                else:
                    tmp+=1
                    if common_idx == len(common_list)-1:
                        common_idx += 1 
                        continue
                    break

        return pairs




    # def __line_diff_check(self, str1, str2):
    #     for i in range len(str1)


