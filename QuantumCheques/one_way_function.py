from cqc.pythonLib import CQCConnection, qubit


def one_way_function(conn, BB84_key, db_id, r, M):
    owf_state = qubit(conn)

    BB84_key = int(BB84_key, 2)
    owf_key = bin(BB84_key)[2:] + bin(db_id)[2:] + bin(r)[2:] + bin(M)[2:]
    owf_key = int(abs(hash(str(owf_key))))
    # p1 , p2, p3 are prime numbers , so coprimes 
    # thus rotation X(key%p1) and Y(key%p2) and Z(key%p3) are independant
    p1 = 33179
    p2 = 32537
    p3 = 31259
    owf_state.rot_X(owf_key%p1%256)
    owf_state.rot_Y(owf_key%p2%256)
    owf_state.rot_Z(owf_key%p3%256)
    return owf_state
