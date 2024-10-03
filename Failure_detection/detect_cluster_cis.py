file_path = "kube-bench-results_after_hardening_20240521_033910.report"

def parse_txt_summary(file_path):
    failed_checks = 0
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("== Summary total =="):
                for _ in range(4):  # Read the next 4 lines for summary details
                    summary_line = next(file).strip()
                    if summary_line.startswith("0 checks FAIL"):
                        failed_checks = int(summary_line.split()[0])
                        print(f"Failed checks: {failed_checks}")
                        break
                    else:
                        print("Failed checks: 1 or more")
                        failed_checks = 1
                        break   
    return failed_checks == 0



parse_txt_summary(file_path)