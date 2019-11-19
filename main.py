from multiprocessing import Process, Pipe

from infra.abstract_view_observer import ViewObserver
from infra.abstract_pathfinder import Pathfinder
from infra.abstract_choreographer import Choreographer


def main():

    vp_conn_1, vp_conn_2 = Pipe()
    vc_conn_1, vc_conn_2 = Pipe()
    pc_conn_1, pc_conn_2 = Pipe()

    view_observer = ViewObserver(vp_conn_1, vc_conn_1)
    pathfinder = Pathfinder(vp_conn_2, pc_conn_1)
    choreographer = Choreographer(vc_conn_2, pc_conn_2)

    view_observer_process = Process(target=view_observer.main)
    pathfinder_process = Process(target=pathfinder.main)
    choreographer_process = Process(target=choreographer.main)

    view_observer_process.start()
    pathfinder_process.start()
    choreographer_process.start()

    view_observer_process.join()
    pathfinder_process.join()
    choreographer_process.join()


if __name__ == '__main__':
    main()
