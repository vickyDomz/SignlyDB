import cv2              # cámara/procesar imágenes
import mediapipe as mp  # puntos de manos y cara
import csv              # manejar archivos csv
import os

mp_hands = mp.solutions.hands           #libreria detecta manos 
mp_draw = mp.solutions.drawing_utils    #libreria que dibuja los puntos y las conexiones entre otros

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)    #procesa los fotogramas var
drawing_spec = mp_draw.DrawingSpec(thickness=1, circle_radius=1) #dibuja los puntos y conexiones var

cap = cv2.VideoCapture(0) #abre la camara

grabando = False          #dependiendo de que es falso o verdadero, va a empezar a grabar la secuencia
secuencia = []            #prepara un futuro conjunto de frames, en los que se hace un gesto
etiqueta = ""             #el nombre del gesto que se esta haciendo ('hola', 'que tal')
sequence_counter = 0      #contador de cuantas veces si hizo el gesto, es como un id

print("Presiona 'e' para ingresar etiqueta del gesto.")
print("Presiona 's' para iniciar/detener grabación.")
print("Presiona 'q' para salir.")

while True:               #mientras grabar sea verdadero
    success, frame = cap.read()    #lee un frame, success es un valor booleano que determina si la leida fue exitosa, y frame es el fotograma leido, ambos son variables, que guardan un valor, este caso, frame lee el fotograma, y success dice si fue exitoso o no.
    if not success: #si no se encontro un frame
        break       #termina el ciclo

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  #pasa el fotograma de BGR a RGB,colores que usa mediapipe
    hand_results = hands.process(rgb_frame) #procesa el fotograma ya cambiado

    # Dibuja puntos
    if hand_results.multi_hand_landmarks:   #revisa si se detectaron manos
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Extrae datos de landmarks
    row = []
    left_hand = [0]*63
    right_hand = [0]*63
    if hand_results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
            base = hand_landmarks.landmark[0]
            coords = []
            for landmark in hand_landmarks.landmark:
                coords += [landmark.x - base.x, landmark.y - base.y, landmark.z - base.z]
            handedness = hand_results.multi_handedness[i].classification[0].label
            if handedness == 'Left':
                left_hand = coords
            else:
                right_hand = coords
        row += left_hand + right_hand
    # Solo guardar si está grabando y hay etiqueta
    if grabando and etiqueta != "":
        secuencia.append(row)

    # Mostrar en pantalla
    texto_estado = "Grabando" if grabando else "Esperando"
    cv2.putText(frame, f"Estado: {texto_estado}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)    #la imagen, el estado del texto el cual cambia si esta grabando o no, la pocicion (x, y), el tipo de letra, el tamano de la letra, el color, el grosor
    cv2.putText(frame, f"Gesto: {etiqueta}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)         #lo mismo
    cv2.imshow("Sign Language Translation", frame)      #el nombre de la ventana

    key = cv2.waitKey(1) & 0xFF #espera de manera permanente una tecla, de un solo caracter
    if key == ord('q'):
        break
    elif key == ord('e'):  # Pide etiqueta nueva
        etiqueta = input("Escribe la etiqueta del gesto que vas a grabar: ")
        print(f"Etiqueta '{etiqueta}' guardada.")
    elif key == ord('s'):  # Start/stop grabación
        if etiqueta == "":
            print("Primero ingresa la etiqueta con 'e'")
        else:
            grabando = not grabando
            if grabando:
                secuencia = []          # limpio secuencia al iniciar grabación
                sequence_counter += 1   # nuevo id de secuencia
            else:
                if len(secuencia) > 0:
                    archivo = f"{etiqueta}.csv"
                    existe = os.path.exists(archivo)
                    with open(archivo, mode='a', newline='') as f:
                        writer = csv.writer(f)
                        if not existe:
                            header = []
                            for h in ('left', 'right'):
                                for i in range(21):
                                    header += [f'{h}_hand_{i}_x', f'{h}_hand_{i}_y', f'{h}_hand_{i}_z']
                        for row_data in secuencia:
                            writer.writerow(row_data + [sequence_counter, etiqueta])  # agrego id y etiqueta
                    print(f"Secuencia guardada en {archivo}, frames: {len(secuencia)}")
                secuencia = []

cap.release()
cv2.destroyAllWindows()