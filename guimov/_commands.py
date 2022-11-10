from guimov import start
from guimov import settings


def _commands_guimov_launch():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--singledataset", help="Dataset path", default=None)
    parser.add_argument("-d", "--datasets", help="Datasets path", default=None)
    parser.add_argument("-l", "--logs", help="Logs path", default=None)
    parser.add_argument("-H", "--host", help="host ip adress", default='0.0.0.0')
    parser.add_argument("-p", "--port", help="host port", default='8050')
    args = parser.parse_args()

    if args.singledataset is not None:
        start(host=args.host, port=args.port, dataset=args.singledataset)
    elif args.datasets is None or args.logs is None:
        raise ValueError('When a single dataset is not provide, datasets path and logs path are required')
    else:
        settings.datasets_path = args.datasets
        settings.logs_path = args.logs
        start(host=args.host, port=args.port)
