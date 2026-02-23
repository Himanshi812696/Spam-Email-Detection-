import binascii
import pickle
import os

fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spam_model.pkl')
print('path:', fp)
print('exists:', os.path.exists(fp))
print('size:', os.path.getsize(fp) if os.path.exists(fp) else 'missing')
with open(fp, 'rb') as f:
    first = f.read(32)
    print('first32 hex:', binascii.hexlify(first))
    f.seek(0)
    try:
        obj = pickle.load(f)
        print('loaded type:', type(obj))
    except Exception as e:
        print('load error:', repr(e))
        try:
            from joblib import load as joblib_load
            print('trying joblib.load fallback...')
            obj2 = joblib_load(fp)
            print('joblib loaded type:', type(obj2))
        except Exception as e2:
            print('joblib load error:', repr(e2))
