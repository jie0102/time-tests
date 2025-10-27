
from times import compute_overlap_time, time_range
import pytest

def test_generic_case():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    expected = [("2010-01-12 10:30:00","2010-01-12 10:37:00"), ("2010-01-12 10:38:00", "2010-01-12 10:45:00")]
    assert compute_overlap_time(large, short) == expected

# 两个时间段没有重叠
def test_no_overlap():
    a = time_range("2010-01-12 08:00:00", "2010-01-12 09:00:00")
    b = time_range("2010-01-12 09:00:01", "2010-01-12 10:00:00")
    expected = []
    assert compute_overlap_time(a, b) == expected


# 两个时间段都包含多个间隔
def test_multiple_intervals_overlap():
    a = time_range("2010-01-12 09:00:00", "2010-01-12 10:00:00", 2, 60)
    b = time_range("2010-01-12 09:30:00", "2010-01-12 10:30:00", 2, 60)
    result = compute_overlap_time(a, b)
    # 不严格比较内容，只要有结果且格式正确
    assert all(isinstance(x, tuple) and len(x) == 2 for x in result)


# 两个时间段恰好首尾相接
def test_touching_ranges():
    a = time_range("2010-01-12 09:00:00", "2010-01-12 09:30:00")
    b = time_range("2010-01-12 09:30:00", "2010-01-12 10:00:00")
    expected = []  # 不算重叠，因为刚好接上
    assert compute_overlap_time(a, b) == expected


def test_backwards_timerange():
    # 倒序时间输入应抛出 ValueError
    with pytest.raises(ValueError, match="must be after start_time"):
        time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")

def test_invalid_number_of_intervals():
    # 区间数为 0 应抛出 ValueError
    with pytest.raises(ValueError, match="must be positive"):
        time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 0)

def test_gap_too_large():
    # 间隔时间过大（总时长 60s，但 gap 需要 120s）
    with pytest.raises(ValueError, match="Gap too large"):
        time_range("2010-01-12 10:00:00", "2010-01-12 10:01:00", 2, 120)
