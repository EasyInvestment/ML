from monitor import monitor
if __name__ == "__main__":
    # offset에 데이터주면 예측값 반환
    monitor("가구","s003800",LabelingValue=20,offset = True)