import sys
import pygame as pg
import numpy as np
import tensorflow as tf


def Train_AI():
    from tensorflow.keras.layers import Input, Dense, Flatten, Dropout, Conv2D
    from tensorflow.keras.models import Model
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0

    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    i = Input(shape=x_train[0].shape)
    x = Conv2D(32, (3, 3), strides=2, activation='relu')(i)
    x = Conv2D(64, (3, 3), strides=2, activation='relu')(x)
    x = Flatten()(x)
    x = Dropout(0.2)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(len(set(y_train)), activation='softmax')(x)

    model = Model(i, x)
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=10)
    model.save('Neural_Net.h5')


# Train_AI()
Model = tf.keras.models.load_model('Neural_Net.h5')


pg.init()
Screen = pg.display.set_mode((448, 448))
menu = pg.image.load('images\\Digits_menu.png').convert_alpha()
font = pg.font.SysFont('consolas', size=25)
draw, prediction = False, ' '

pic = np.zeros((28, 28), dtype=int)
zoom_pic = np.repeat(np.repeat(pic, 16, axis=0), 16, axis=1)
zoom_pre_pic = zoom_pic.copy()
if __name__ == '__main__':
    while True:
        Screen.blit(menu, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            mx, my = pg.mouse.get_pos()
            if (event.type == pg.MOUSEBUTTONDOWN) and (event.button == 1):
                if (77 <= mx <= 213) and (399 <= my <= 432):
                    prediction = str(np.argmax(Model.predict(np.expand_dims(pic.T / 255.0, axis=0))))
                elif (234 <= mx <= 370) and (399 <= my <= 432):
                    pic = np.zeros((28, 28), dtype=int)
                    Screen.fill((0, 0, 0))
                    prediction = ' '
                else:
                    draw = True
            if (event.type == pg.MOUSEBUTTONUP) and (event.button == 1):
                draw = False
        tool_text = font.render(prediction, True, (253, 236, 166))
        tool_text_rect = tool_text.get_rect(center=(224, 33))
        Screen.blit(tool_text, tool_text_rect)

        if draw:
            mx, my = pg.mouse.get_pos()
            current = pic[int(mx/16-2):int(mx/16+3), int(my/16-2):int(my/16+3)]
            kernal = np.array([[0, 0, 1, 0, 0], [0, 1, 2, 1, 0], [1, 2, 10, 2, 1], [0, 1, 2, 1, 0], [0, 0, 1, 0, 0]])
            f = np.vectorize(lambda x, y: x + y if x + y < 254 else 254)
            try:
                update = f(kernal*6, current)
                pic[int(mx / 16 - 2):int(mx / 16 + 3), int(my / 16 - 2):int(my / 16 + 3)] = update
                zoom_pre_pic = zoom_pic.copy()
                zoom_pic = np.repeat(np.repeat(pic, 16, axis=0), 16, axis=1)
            except ValueError:
                pass
        data = np.where(zoom_pre_pic != zoom_pic)
        for a, b in zip(data[0], data[1]):
            color = zoom_pic[a, b]
            Screen.fill((color, color, color), ([a, b], (1, 1)))
        zoom_pre_pic = zoom_pic.copy()
        pg.display.update()

