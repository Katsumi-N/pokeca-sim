# 参考にしたサイト
# Qiita "PySimpleGUIの基本的な使用方法"https://qiita.com/KatsunoriNakamura/items/376da645e52f7ef7f9ef
# Trinket "Graph Element" https://pysimplegui.trinket.io/demo-programs#/graph-element/graph-element-drawing-and-dragging
import argparse
import PySimpleGUI as sg
import random
from pokeca_scraping import scraping

def start(graph, deck_copy, deck_list_copy):
    deck = deck_copy
    deck_list = deck_list_copy[:]
    random.shuffle(deck_list)

    # サイドを6枚, ハンド7枚
    side = [deck_list.pop() for _ in range(6)]
    hand = [deck_list.pop() for _ in range(7)]

    # 手札を7枚引く
    for i in range(7):
        graph.draw_image(filename=deck[hand[i]][2], location=(150+ i*70, 100))
        deck[hand[i]][0] -= 1
    # サイド
    side_loc = [(110, 250), (180, 250), (110, 330), (180, 330), (110, 410), (180, 410)]
    for i in range(6):
        graph.draw_image(filename=deck[side[i]][2], location=side_loc[i])
        deck[side[i]][0] -= 1

    return deck, deck_list

def shuffle(deck_list):
    random.shuffle(deck_list)
    print("shuffle")

def draw(graph, deck, deck_list):
    draw_card = deck_list.pop()
    deck[draw_card][0] -= 1
    graph.draw_image(filename=deck[draw_card][2], location=(680, 230))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deck_code",
        type=str,
        default="kVVF5w-bueC8Z-FFVvkF",
    )
    parser.add_argument(
        "--driver_dir",
        type=str,
        default="C:\\Users\\naya-\\Anaconda3\\envs\\rl\\Lib\\site-packages\\chromedriver_binary\\chromedriver.exe"
    )
    args = parser.parse_args()


    sg.theme('Dark Blue 3')
    layout = [[sg.Graph(
        canvas_size=(900, 500),
        graph_bottom_left=(0, 0),
        graph_top_right=(900, 500),
        key="-GRAPH-",
        change_submits=True,  # mouse click events
        background_color='lightblue',
        drag_submits=True)],
        [sg.Button("Reset"), sg.Button("Shuffle"), sg.Button("Draw"), sg.Button("See Deck"),
         sg.Button("Pick 1 card"), sg.Button("Exit")]
    ]

    window = sg.Window("Pokemon-card simulator", layout, finalize=True)

    # get the graph element for ease of use later
    graph = window["-GRAPH-"]  # type: sg.Graph

    graph.draw_text("手札", (370, 120))
    graph.draw_rectangle((100, 130),(650, 10))

    graph.draw_text("サイド", (170, 410))
    graph.draw_rectangle((100, 430), (250, 150))

    graph.draw_text("ベンチ", (450, 280))
    graph.draw_rectangle((260, 300), (650, 150))

    graph.draw_text("バトル場", (440, 400))
    graph.draw_rectangle((400, 410), (480, 310))

    graph.draw_text("トラッシュ", (710, 120))
    graph.draw_rectangle((670, 130), (750, 10))

    graph.draw_text("山札", (710, 270))
    graph.draw_rectangle((670, 280), (750, 150))

    dragging = False
    start_point = end_point = prior_rect = None

    #deck(キーが名前、値が枚数), deck_list(カードの名前を格納したリスト)を取得
    deck, deck_list = scraping(args.deck_code, args.driver_dir)

    #デッキ(キーが名前、値が枚数)とデッキリスト(リスト)のコピーを作成
    deck_list_copy = deck_list[:]
    deck_copy = deck.copy()

    deck, deck_list = start(graph, deck_copy, deck_list_copy)

    while True:
        event, values = window.read()
        if event is None:
            break  # exit
        if event == "-GRAPH-":  # if there's a "Graph" event, then it's a mouse
            x, y = values["-GRAPH-"]
            if not dragging:
                start_point = (x, y)
                dragging = True
                drag_figures = graph.get_figures_at_location((x,y))
                lastxy = x, y
            else:
                end_point = (x, y)
            if prior_rect:
                graph.delete_figure(prior_rect)
            delta_x, delta_y = x - lastxy[0], y - lastxy[1]
            lastxy = x,y
            for fig in drag_figures:
                graph.move_figure(fig, delta_x, delta_y)
                graph.update()

        elif event.endswith('+UP'):  # The drawing has ended because mouse up
            start_point, end_point = None, None  # enable grabbing a new rect
            dragging = False
            prior_rect = None

        if event == "Reset":
            graph.erase()
            deck, deck_list = start(graph, deck_copy, deck_list_copy)

        if event == "Shuffle":
            shuffle(deck_list)

        if event == "Draw":
            draw(graph, deck, deck_list)

        if event == "See Deck":
            print(deck)

        if event == "Pick 1 card":
            card_name = sg.PopupGetText('デッキから持ってくるカード名を入力してください')
            # assert card_name in set(deck_list), 'デッキ内のカードを指定してください'
            if card_name in set(deck_list):
                deck_list.remove(card_name)
                graph.draw_image(filename=deck[card_name][2], location=(680, 230))
                deck[card_name][0] -= 1
            else:
                print('デッキ内のカードを指定してください')

        if event == "Exit":
            break


    window.close()

if __name__ == '__main__':
    main()