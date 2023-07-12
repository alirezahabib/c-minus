


def tester(first_file_path, second_file_path):
    # print("begining")
    #open each file
    first_file = open(first_file_path, "r+",encoding='utf-8')
    second_file = open(second_file_path, "r+",encoding='utf-8')
    #read each file
    # first_file.seek(0)
    # second_file.seek(0)
    # print("there")
    first_file_lines = first_file.read().splitlines()
    second_file_lines = second_file.read().splitlines()
    # if both are equal print pass otherwise fail
    # if first_file_lines == None or second_file_lines == None:
    #     print("kir")
    # print('here')
    # print("first_file_lines", first_file_lines)
    # print("second_file_lines", second_file_lines)
    if first_file_lines[-1]=='':
        first_file_lines.pop()
    if second_file_lines[-1]=='':
        second_file_lines.pop()
    # # print(second_file_lines[-1])
    # # print(first_file_lines[-1])
    # if '\n' in first_file_lines:
    #     first_file_lines.remove('\n')
    #
    # if '\n' in second_file_lines:
    #     second_file_lines.remove('\n')
    # print("first_file_lines", first_file_lines)
    # print("second_file_lines", second_file_lines)
    if first_file_lines == second_file_lines:
        first_file.close()
        second_file.close()
        return "pass"
    else:
        first_file.close()
        second_file.close()
        return "fail"
    #close each file
    # first_file.close()
    # second_file.close()
# print("now?")
cnt_cg = 0
cnt_sa = 0
for i in range(10):

    a = i+1
    print("testcase ",a, end=": ")
    res = tester(f"code_generation/expected{a}.txt", f"code_generation/out{a}.txt")
    if res == "pass":
        cnt_cg += 1
    print(res)
    print("semantic test case ",a, end=": ")
    res_semantic_analyzer = tester(f"semantic_analyzer/S{a}/semantic_errors.txt", f"semantic_analyzer/semantic_errors{a}.txt")
    if res_semantic_analyzer == "pass":
        cnt_sa += 1
    print(res_semantic_analyzer)
print()
print("tests finished, reslut:")
print("code generation: ", cnt_cg, "/10")
print("semantic analyzer: ", cnt_sa, "/10")
# tester("code_generation/expected2.txt", "code_generation/out2.txt")

# if __name__ == "main":
#     print("main")
#     tester("code_generation/expected10.txt", "code_generation/out10.txt")
#     # for i in range(10):
#     #     a = i+1
#     #     tester(f"code_generation/expected{a}.txt", f"code_generation/out{a}.txt")