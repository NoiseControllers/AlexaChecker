import argparse
from multiprocessing import Manager
from queue import Queue

from src.Controllers.CheckAlexaRank import CheckAlexaRank
from src.Controllers.ProxyController import ProxyController
from src.Utils.File import read_file, output_file
from src.Utils.SortList import take_second


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Fichero de entrada.', dest='input_file', type=str, required=True)
    parser.add_argument('-o', '--output', help='Fichero de salida.', dest='output_filename', type=str)
    parser.add_argument('-t', '--threads', help='Numero de hilos a usar.', dest='threads', type=int)
    parser.add_argument('-p', '--proxies', help='Fichero proxies (socks4).', dest='proxies_filename', type=str)

    args = parser.parse_args()
    main_file = args.input_file
    output_filename = args.output_filename or "out.xlsx"
    maximum_threads = args.threads or 1
    proxies_filename = args.proxies_filename or None

    proxy_controller = None

    if proxies_filename is not None:
        proxy_controller = ProxyController(type_sock="socks4", proxies=read_file(path=proxies_filename))

    threads = []
    urls_queue = Queue()

    with Manager() as manager:
        output_list = manager.list()

        for t in range(maximum_threads):
            thread = CheckAlexaRank(queue=urls_queue, output_list=output_list, proxy_controller=proxy_controller)
            thread.daemon = True
            thread.start()
            threads.append(thread)

        # Load input file
        for url in read_file(main_file):
            urls_queue.put(url)

        urls_queue.join()

        for x in range(maximum_threads):
            urls_queue.put(None)

        for t in threads:
            t.join()

        # save file
        output_list.sort(key=take_second)
        output_file(filename=output_filename, data_list=output_list)
        print("[+] Finished process")


if __name__ == '__main__':
    main()
