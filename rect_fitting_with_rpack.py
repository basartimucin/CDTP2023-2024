from rectpack import newPacker, MaxRectsBaf, GuillotineBssfSas, GuillotineBafSas, MaxRectsBl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import time

from gcode_gen import write_gcode


def read_rects(file_name):
    rectangles = []
    size = 0
    bin_width, bin_height = 0, 0
    try:
        with open(file_name, 'r') as file:
            size = int(file.readline().strip('\n'))

            if size > 0:
                bin_width, bin_height = map(int, file.readline().strip().split())

                rectangles = []
                for line in file:
                    # Satırın boş olup olmadığını kontrol et
                    if line.strip():
                        x, y = map(int, line.strip().split())
                        rectangles.append((x, y))

                # print("Dosya başarıyla okundu ve demet dizisi oluşturuldu:", rectangles)
            else:
                print("Hata: Dosya boş veya eksik veri içeriyor.")
    except FileNotFoundError:
        print(f"Hata: Dosya '{file_name}' bulunamadı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    # try:
    #     with open(file_name, 'r') as file:
    #         size = int(file.readline().strip('\n'))
    #         line = file.readline().strip()
    #         bin_width,bin_height = map(int,line.split())
    #         rectangles = [(int(x), int(y)) for x, y in (line.split() for line in file)]
    #         #print(rectangles)
    #     #print("Belge başarılı bir şekilde okundu ve tuplelar oluşturuldu:", rectangles)
    # except FileNotFoundError:
    #     print(f"Error: File '{file_name}' not found.")
    # except Exception as e:
    #     print(f"Bir hata meydana geldi: {e}")

    packed_rectangles = pack_rects(rectangles, bin_width, bin_height, size)
    return packed_rectangles, bin_width, bin_height, size


def pack_rects(rectangles, bin_width, bin_height, size):
    start_time = time.time()  # sayaç başlat

    # print("dikdörtgen sayısı: " + str(len(rectangles)))
    # en sağa ve en alta yerleştirmeye yönelik pack_algo ile bir packer oluşturuyoruz.
    packer = newPacker(pack_algo=MaxRectsBl, rotation=True)

    for r in rectangles:
        packer.add_rect(*r)

    packer.add_bin(bin_width, bin_height)

    packer.pack()

    packed_rectangles = packer.rect_list()

    end_time = time.time()  # sayaç durdur
    elapsed_time = end_time - start_time

    show_graphic(packed_rectangles, bin_width, bin_height, size, elapsed_time)

    return packed_rectangles


def random_color():
    return (random.random(), random.random(), random.random())


def show_graphic(packed_rectangles, bin_width, bin_height, rectangle_size, elapsed_time):
    plt.figure()
    ax = plt.gca()
    count = 0
    for rect in packed_rectangles:
        count += 1
        x, y, w, h = rect[1], rect[2], rect[3], rect[4]
        rect = plt.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor=random_color())
        ax.add_patch(rect)


    # write count to title
    plt.suptitle("Bütün Dikdörtgenler Sayisi: " + str(rectangle_size), fontsize=12)
    plt.title("Yerleştirilen Dikdörtgenler Sayisi: " + str(count))

    efficiency = count / rectangle_size
    Benchmark(rectangle_size, count, efficiency, elapsed_time)

    plt.xlim(0, bin_width)
    plt.ylim(0, bin_height)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def Benchmark(rectangle_size, count, efficiency, elapsed_time):
    print(f"Toplam dikdörtgen sayısı ", rectangle_size)
    print(f"Yerleştirilen Dikdörtgenler Sayisi:", count)
    print(f"Yerleştirilen dikdörtgen / Toplam Dikdörgen oranı ", efficiency)
    print(f"grafik oluşturulana kadar geçen süre: {elapsed_time} saniye")


if __name__ == "__main__":
    basename = "Original/C"
    for i in range(1, 8):
        for j in range(1, 4):
            filename = basename + str(i) + "_" + str(j)
            # print("Testing: ", str(i) + "_" + str(j))

            if i == 1 and j <= 3:
                packed_rectangles, bin_width, bin_height, size = read_rects(filename)
                write_gcode(packed_rectangles, bin_width, bin_height, size, f"output C{i}_{j}")

            else:
                read_rects(filename)
