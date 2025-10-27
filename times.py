import datetime


def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    if end_time_s <= start_time_s:
       raise ValueError("start time should be before end")
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]


import datetime

def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            # 将字符串转为 datetime，不修改原变量
            s1 = datetime.datetime.strptime(start1, "%Y-%m-%d %H:%M:%S") if isinstance(start1, str) else start1
            e1 = datetime.datetime.strptime(end1, "%Y-%m-%d %H:%M:%S") if isinstance(end1, str) else end1
            s2 = datetime.datetime.strptime(start2, "%Y-%m-%d %H:%M:%S") if isinstance(start2, str) else start2
            e2 = datetime.datetime.strptime(end2, "%Y-%m-%d %H:%M:%S") if isinstance(end2, str) else end2

            # 计算重叠区间
            low = max(s1, s2)
            high = min(e1, e2)

            # ✅ 只保留真正重叠部分（low < high）
            if low < high:
                overlap_time.append(
                    (low.strftime("%Y-%m-%d %H:%M:%S"), high.strftime("%Y-%m-%d %H:%M:%S"))
                )

    return overlap_time



if __name__ == "__main__":
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    print(compute_overlap_time(large, short))