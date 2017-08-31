'''
   ファイルの読み込み・保存を行う関数
'''
import pickle

def load_pickle(path):
    f = open(path, 'rb')
    output = pickle.load(f)
    f.close()
    return output

def save_model(model,path):
    f = open(path, 'wb')
    pickle.dump(model,f)
    f.close()