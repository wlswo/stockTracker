from datetime import datetime, timedelta


def get_time_range():
  """ 어제 오후 10시 ~ 오늘 새벽 6시의 시간을 'YYYYMMDDTHHMM' 형식으로 반환 """
  now = datetime.now()

  # 어제 오후 10시 (22:00)
  time_from = now.replace(hour=22, minute=0, second=0) - timedelta(days=2)

  # 오늘 새벽 6시 (06:00)
  time_to = now.replace(hour=6, minute=0, second=0)

  # 형식 변환 (YYYYMMDDTHHMM)
  time_from_str = time_from.strftime("%Y%m%dT%H%M")
  time_to_str = time_to.strftime("%Y%m%dT%H%M")

  return time_from_str, time_to_str
