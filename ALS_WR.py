import pandas as pd
import numpy as np
import pickle
import os
import argparse
from scipy import sparse
from scipy.sparse import linalg, lil_matrix, csr_matrix
from module import load_pickle, save_model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', '-e', type=int,
                        help='epoch数の指定')
    parser.add_argument('--noize_rate', '-r', type=float,
                        help='正則化項の倍率指定')
    parser.add_argument('--common_len', '-c', type=int,
                        help='共通列の長さ指定')
    parser.add_argument('--output_path', '-p', type=str, default='output',
                        help='modelの保存場所指定')
    args = parser.parse_args()

    id_rating = load_pickle('data/id_rating.pickle')
    id_test_rating = load_pickle('data/id_test_rating.pickle')
    id_rating_np = load_pickle('data/id_rating_np.pickle')
    rating_test_pair = load_pickle('data/rating_test_pair.pickle')

    id_rating_lil = lil_matrix(id_rating_np)
    del id_rating_np
    common_len = args.common_len
    u_len, m_len = id_rating_lil.shape
    I = id_rating_lil > 0
    u = np.random.uniform(0, 5, u_len * common_len).reshape(u_len, common_len)
    m = np.random.uniform(0, 5, m_len * common_len).reshape(common_len, m_len)
    u = lil_matrix(u).tocsr()
    m = lil_matrix(m).tocsc()
    noize_rate = args.noize_rate
    # 全データ数が100000でテスト用には各userのratingが１つだけ入っている
    training_len = 100000 - u_len
    test_len = u_len
    
    # training
    for epoch in range(args.epochs):
        for i in range(u_len):
            I_i = np.array(I.getrow(i).todense())[0]
            u[i] = (linalg.inv(m[:,I_i].dot(m[:,I_i].T)+
                                  noize_rate*I[i].sum()*
                                  sparse.eye(common_len))).dot(
            m[:,I_i].dot(id_rating_lil[i,I_i].transpose())).transpose()

        for j in range(m_len):
            I_j = np.array(I.transpose().getrow(j).todense())[0]
            m[:,j] = (linalg.inv(u[I_j].T.dot(u[I_j]) +
                                      noize_rate*I[:,j].sum()*
                                    sparse.eye(common_len))).dot(
            u[I_j].transpose().dot(id_rating_lil[I_j,j]).todense())
        # predict
        pred = u.dot(m)
    
        # rmse
        loss = np.sqrt((np.power((id_rating_lil - pred)[I],2).sum()/training_len))
                   
        # test_loss
        test_loss = 0
        for pair in rating_test_pair:
            true_rating = rating_test_pair[pair]
            test_loss += ((true_rating-pred[pair[0]-1,pair[1]-1])**2)/test_len

        print('epoch : {0:>3}, loss : {1:.7f}, test_loss : {2:.7f}'\
              .format(epoch+1, loss, np.sqrt(float(test_loss))))

    save_model(u, os.path.join(args.output_path, 'u.pickle'))
    save_model(m, os.path.join(args.output_path, 'm.pickle'))


if __name__ == '__main__':
    main()
