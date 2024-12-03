import os
import cv2 as cv
import numpy as np

def load_stickers():
    """Carrega stickers do diretório especificado."""
    print("Escolha seu Sticker:")
    print("1. Touca de Natal\n2. Óculos\n3. Papai Noel\n4. Neve\n5. Sol")

    choice = input("Escolha uma opção: ")
    sticker_dir = f"C:\\Users\\aaleknovic\\Pictures\\strickers\\{choice}"
    
    stickers = []
    if not os.path.exists(sticker_dir):
        print("Diretório não encontrado.")
        return stickers

    for file in os.listdir(sticker_dir):
        if file.endswith(".png"):
            sticker = cv.imread(os.path.join(sticker_dir, file), cv.IMREAD_UNCHANGED)
            if sticker is not None:
                stickers.append(sticker)

    return stickers

def apply_sticker(image, sticker, x, y):
    """Aplica um sticker transparente em uma posição especificada."""
    h, w = sticker.shape[:2]

    # Verifica se o sticker está dentro dos limites da imagem
    if y + h > image.shape[0] or x + w > image.shape[1] or x < 0 or y < 0:
        return image

    overlay = image[y:y+h, x:x+w]

    # Calcula a transparência
    alpha_sticker = sticker[:, :, 3] / 255.0
    alpha_image = 1.0 - alpha_sticker

    for c in range(3):
        overlay[:, :, c] = (alpha_sticker * sticker[:, :, c] + alpha_image * overlay[:, :, c])

    image[y:y+h, x:x+w] = overlay
    return image

def apply_filter(image, filter_type):
    """Aplica diferentes filtros na imagem."""
    if filter_type == '1':
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # Filtro em escala de cinza
    elif filter_type == '2':
        return cv.GaussianBlur(image, (15, 15), 0)  # Filtro de desfoque
    elif filter_type == '3':
        return cv.Canny(image, 100, 200)  # Detecção de bordas
    elif filter_type == '4':
        return cv.medianBlur(image, 15)  # Filtro de desfoque mediano
    elif filter_type == '5':
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        return cv.filter2D(image, -1, kernel)  # Filtro de nitidez
    elif filter_type == '6':
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        hsv[:, :, 2] = cv.equalizeHist(hsv[:, :, 2])
        return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)  # Filtro de equalização
    elif filter_type == '7':
        return cv.bilateralFilter(image, 15, 75, 75)  # Filtro bilateral
    elif filter_type == '8':
        return cv.bitwise_not(image)  # Inversão de cores
    elif filter_type == '9':
        return cv.applyColorMap(image, cv.COLORMAP_JET)  # Mapa de cores JET
    elif filter_type == '10':
        return cv.Laplacian(image, cv.CV_64F)  # Detecção de bordas Laplacian
    else:
        print("Filtro inválido.")
        return image

def draw_interface(image, stickers, selected_sticker):
    """Desenha a interface para visualização dos stickers."""
    preview = cv.resize(stickers[selected_sticker], (50, 50))
    image[0:50, 0:50] = preview[:, :, :3]
    cv.putText(image, f"Sticker: {selected_sticker + 1}", (60, 30),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

def main():
    print("Você deseja adicionar filtros ou stickers em suas imagens?")
    print("1. Stickers\n2. Filtros")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        print("1. Carregar imagem\n2. Capturar vídeo pela webcam")
        input_choice = input("Escolha uma opção: ")

        if input_choice == "1":
            file_path = input("Digite o caminho da imagem: ")
            image = cv.imread(file_path)
            if image is None:
                print("Erro ao carregar a imagem.")
                return

        elif input_choice == "2":
            cap = cv.VideoCapture(0)
            if not cap.isOpened():
                print("Erro ao acessar a webcam.")
                return

            ret, image = cap.read()
            cap.release()

            if not ret:
                print("Erro ao capturar imagem da webcam.")
                return

        else:
            print("Opção inválida.")
            return

        stickers = load_stickers()
        if not stickers:
            print("Nenhum sticker encontrado no diretório especificado.")
            return

        selected_sticker = 0
        current_x, current_y = 100, 100

        def mouse_callback(event, x, y, flags, param):
            nonlocal current_x, current_y
            if event == cv.EVENT_LBUTTONDOWN or event == cv.EVENT_MOUSEMOVE:
                current_x, current_y = x, y

        cv.namedWindow("Editor")
        cv.setMouseCallback("Editor", mouse_callback)

        while True:
            temp_image = image.copy()
            draw_interface(temp_image, stickers, selected_sticker)

            temp_image = apply_sticker(temp_image, stickers[selected_sticker], current_x, current_y)

            cv.imshow("Editor", temp_image)
            key = cv.waitKey(1) & 0xFF

            if key == ord('s'):
                save_path = input("Digite o caminho para salvar a imagem: ")
                cv.imwrite(save_path, temp_image)
                print("Imagem salva com sucesso!")
            elif key == ord('a'):
                selected_sticker = (selected_sticker - 1) % len(stickers)
            elif key == ord('d'):
                selected_sticker = (selected_sticker + 1) % len(stickers)

        

        cv.destroyAllWindows()

    elif choice == '2':

        print("1. Carregar imagem\n2. Capturar vídeo pela webcam")
        input_choice = input("Escolha uma opção: ")

        if input_choice == "1":
            file_path = input("Digite o caminho da imagem: ")
            image = cv.imread(file_path)
            if image is None:
                print("Erro ao carregar a imagem.")
                return

        elif input_choice == "2":
            cap = cv.VideoCapture(0)
            if not cap.isOpened():
                print("Erro ao acessar a webcam.")
                return

            ret, image = cap.read()
            cap.release()

            if not ret:
                print("Erro ao capturar imagem da webcam.")
                return
        print("Escolha um dos filtros abaixo:")
        print("1. Escala de cinza\n2. Desfoque\n3. Detecção de bordas\n4. Desfoque mediano\n5. Nitidez")
        print("6. Equalização\n7. Filtro bilateral\n8. Inversão de cores\n9. Mapa de cores JET\n10. Laplacian")
        filter_choice = input("Escolha um filtro: ")

        filtered_image = apply_filter(image, filter_choice)

        cv.imshow("Imagem com Filtro", filtered_image)
        key = cv.waitKey(0)

        if key == ord('s'):          
            save_path = input("Digite o caminho para salvar a imagem: ")
            cv.imwrite(save_path, filtered_image)
            print("Imagem salva com sucesso!")
            cv.destroyAllWindows()

    else:
       print("Opção inválida.")


if __name__ == "__main__":
    main()
