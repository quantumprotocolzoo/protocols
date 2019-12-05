from one_way_function import one_way_function
from cqc.pythonLib import CQCConnection, qubit
import random
import tqdm


def T(q):
    # T = RZ(pi/4) * e(i*pi/8)
    q.rot_Z(256//8)
    return


def invT(q):
    # T* == RZ(-pi/4) * e(i*pi/8)
    q.rot_Z(256 - 256//8)
    return


def CSWAP(q0, q1, q2):
    # fredkin implementation from :
    # https://www.mathstat.dal.ca/~selinger/quipper/doc/QuipperLib-GateDecompositions.html
    q2.cnot(q1)
    q2.H()
    T(q0)
    T(q1)
    T(q2)
    q1.cnot(q0)
    q2.cnot(q1)
    q0.cnot(q2)
    invT(q1)
    T(q2)
    q0.cnot(q1)
    invT(q0)
    invT(q1)
    q2.cnot(q1)
    q0.cnot(q2)
    q1.cnot(q0)
    q2.H()
    q2.cnot(q1)
    return


def swap_test(conn, q1, q2):
    # swap_test implementation from :
    # https://en.wikipedia.org/wiki/Swap_test

    q0 = qubit(conn)
    q0.H()
    CSWAP(q0, q1, q2)
    q0.H()
    m = q0.measure()

    # collaspse everything after swap_test to avoid :
    # cqc.pythonLib.CQCNoQubitError: No more qubits available
    q1.measure()
    q2.measure()
           
    return m


def main():
    # Initialize the connection
    with CQCConnection("Alice") as Alice:
        BB84_key = 2
        db_id = 1
        M = 2
        res_same = []
        res_diff = []
        for i in tqdm.tqdm(range(1000)):
            salt = random.randint(0, 1000)
            epsilon = random.randint(1,10)
            q1 = one_way_function(Alice, BB84_key, db_id, salt, M)
            q2 = one_way_function(Alice, BB84_key, db_id, salt, M)
            m_same = swap_test(Alice, q1,q2)
            q1 = one_way_function(Alice, BB84_key, db_id, salt, M)
            q2 = one_way_function(Alice, BB84_key, db_id, salt + epsilon, M)
            m_diff = swap_test(Alice, q1,q2)
            res_same.append(m_same)
            res_diff.append(m_diff)
            print(res_same,res_diff)
    score_same = sum(res_same)/len(res_same)
    score_diff = sum(res_diff)/len(res_diff)
    print('swap_test score for identical state', score_same)
    print('swap_test score for different state', score_diff)


if __name__ == "__main__":
    # execute only if run as a script
    main()

