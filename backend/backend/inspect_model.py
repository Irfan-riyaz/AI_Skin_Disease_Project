from tensorflow import keras
import numpy as np, os
p = r"models\Skin_Cancer_Model.h5"
print('Loading model from', os.path.abspath(p))
m = keras.models.load_model(p)
print('Loaded model')
try:
    print('INPUT_SHAPE:', getattr(m, 'input_shape', None))
    print('OUTPUT_SHAPE:', getattr(m, 'output_shape', None))
except Exception as e:
    print('Error reading shapes:', e)
print('\nLast 5 layers:')
for layer in m.layers[-5:]:
    try:
        print(' -', layer.name, getattr(layer, 'output_shape', ''))
    except:
        print(' -', layer.name)

# Build a random input matching shape
inp_shape = m.input_shape
if inp_shape is None:
    print('Model has no input_shape attribute')
else:
    bs = 1
    shape = []
    for s in inp_shape[1:]:
        if s is None:
            shape.append(224)
        else:
            shape.append(s)
    batch = (bs,)+tuple(shape)
    print('Using random input shape:', batch)
    x = np.random.rand(*batch).astype('float32')
    try:
        pred = m.predict(x)
        print('PRED_SHAPE:', np.array(pred).shape)
        flat = np.array(pred).flatten()
        print('PRED_SAMPLE:', flat[:10])
    except Exception as e:
        print('Error during sample predict:', e)
