from StockDataLoad import FinanceData
from GetData import dataAll
from Network import ensembleModel
from dataIndicator import *
from sklearn.preprocessing import StandardScaler
def monitor(category,stockName,LabelingValue = 120,seq_len = 20,offset = True):
    # 데이터 업데이트
    # FinanceData()

    # 데이터 불러오기
    stockData = dataAll(category,stockName)
    stockData = stockData.drop(["timestamp"],axis=1)
    stockData.columns = [curr_name.lower() for curr_name in stockData.columns]

    # 데이터 라벨링
    from DataLabeling import DataLabeling
    labeling = DataLabeling(stockData, LabelingValue, "close")
    labeling.run()
    data = labeling.data

    # 보조지표 추가
    data = add_rsi(data)
    data = add_ma(data,period=7)
    data = add_ema(data,period=7)
    data = add_ma(data,period=25)
    data = add_ema(data,period=25)
    data = add_ma(data,period=99)
    data = add_ema(data,period=99)
    data = add_stochastic(data)
    data = add_bb(data,length=21)
    data = add_disparity(data,period=25)
    data = add_macd(data)
    data = add_kdj(data)
    data = data.dropna()


    X,Y = data.drop(['label'],axis = 1),data['label']
    X = StandardScaler().fit_transform(X)
    # 데이터 분리
    if offset == True:
        test_size = int(len(data) * 0.2)
        x_train = X[:test_size]
        y_train = Y[:test_size]
        x_test = X[test_size:]
        y_test = Y[test_size:]
    else:
        x_train,y_train = X,Y
    
    # 모델 학습
    model = ensembleModel(seq_len,x_train.shape[1])
    model.models_fit(x_train,y_train)

    if offset == True:
        from sklearn.metrics import classification_report
        pred = model.predict_and_evaluation(x_test,y_test)
        result = []
        for i in range(len(model.LSTMPredict)):
            curr_pred = model.LSTMPredict[i]
            if curr_pred < 0.5:
                result.append(0)
            else:
                result.append(1)
        print(classification_report(result,y_test.tolist()))
    else:
        model.predict(offset)
