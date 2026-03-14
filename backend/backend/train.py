import os
import argparse
import json
import math
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def build_model(num_classes, input_shape=(224, 224, 3), base_model_name='EfficientNetB0', dropout=0.4):
    if base_model_name == 'EfficientNetB0':
        base = tf.keras.applications.EfficientNetB0(include_top=False, input_shape=input_shape, weights='imagenet')
    else:
        base = tf.keras.applications.MobileNetV2(include_top=False, input_shape=input_shape, weights='imagenet')

    base.trainable = False
    x = layers.GlobalAveragePooling2D()(base.output)
    x = layers.Dropout(dropout)(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.Dropout(dropout * 0.5)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    model = keras.models.Model(inputs=base.input, outputs=outputs)
    return model


def get_dataset(data_dir, img_size=(224, 224), batch_size=32, val_split=0.2, seed=123):
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="training",
        seed=seed,
        image_size=img_size,
        batch_size=batch_size
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="validation",
        seed=seed,
        image_size=img_size,
        batch_size=batch_size
    )

    AUTOTUNE = tf.data.AUTOTUNE
    class_names = train_ds.class_names if hasattr(train_ds, 'class_names') else []
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
    return train_ds, val_ds, class_names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, required=True, help='Directory with subfolders per class')
    parser.add_argument('--output', type=str, default='models/multi_class_model.h5')
    parser.add_argument('--classes_out', type=str, default='models/classes.txt')
    parser.add_argument('--img_size', type=int, default=224)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--epochs', type=int, default=20)
    parser.add_argument('--base', type=str, default='EfficientNetB0')
    parser.add_argument('--dropout', type=float, default=0.4)
    parser.add_argument('--save_best_only', action='store_true')

    args = parser.parse_args()

    data_dir = args.data_dir
    assert os.path.isdir(data_dir), f"data_dir not found: {data_dir}"

    train_ds, val_ds, class_names = get_dataset(data_dir, img_size=(args.img_size, args.img_size), batch_size=args.batch_size)
    print(f"Detected {len(class_names)} classes")
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.classes_out, 'w', encoding='utf-8') as fh:
        for c in class_names:
            fh.write(c + '\n')
    print(f"Wrote classes list to {args.classes_out}")

    model = build_model(len(class_names), input_shape=(args.img_size, args.img_size, 3), base_model_name=args.base, dropout=args.dropout)
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-4), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    callbacks = []
    ckpt = keras.callbacks.ModelCheckpoint(args.output, save_best_only=args.save_best_only, monitor='val_accuracy', mode='max')
    callbacks.append(ckpt)
    callbacks.append(keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3))
    callbacks.append(keras.callbacks.EarlyStopping(monitor='val_loss', patience=6, restore_best_weights=True))

    history = model.fit(train_ds, validation_data=val_ds, epochs=args.epochs, callbacks=callbacks)

    # Save final model (if not using save_best_only)
    if not args.save_best_only:
        model.save(args.output)
        print(f"Saved model to {args.output}")

    # Optionally unfreeze and fine-tune
    print('Training complete')


if __name__ == '__main__':
    main()
