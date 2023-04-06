import requests
import argparse


def create(create_args: argparse.Namespace):
    domain = create_args.domain
    file_path = create_args.file_path
    url = f"http://{domain}/user"
    with open(file_path, 'rb') as f:
        file_obj = {'file': f}
        response = requests.post(url, files=file_obj)
    print(response.text)


def get(get_args: argparse.Namespace):
    user_id = get_args.id
    domain = get_args.domain
    url = f"http://{domain}/user/{user_id}"
    response = requests.get(url)
    print(response.text)


def update(update_args):
    domain = update_args.domain
    user_id = update_args.id
    file_path = update_args.file_path
    url = f"http://{domain}/user/{user_id}"
    with open(file_path, 'rb') as f:
        file_obj = {'file': f}
        response = requests.put(url, files=file_obj)
    print(response.text)


def delete(delete_args):
    user_id = delete_args.id
    domain = delete_args.domain
    url = f"http://{domain}/user/{user_id}"
    response = requests.delete(url)
    print(response.text)


def main(args):
    if args.action == 'create':
        create(args)
    elif args.action == 'delete':
        delete(args)
    elif args.action == 'update':
        update(args)
    elif args.action == 'get':
        get(args)
    else:
        print('invalid action')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI utility which communicates with user-crud services')
    subparsers = parser.add_subparsers(dest='action', help='Available actions')

    # create command to create a user
    create_parser = subparsers.add_parser('create', help='Create a user')
    create_parser.add_argument('-f', '--file-path', type=str, help='file contains user details', required=True)
    create_parser.add_argument('-d', '--domain', type=str, help='specify domain using --domain argument',
                               required=True)

    # update command to update a user
    update_parser = subparsers.add_parser('update', help='Update a user')
    update_parser.add_argument('--id', type=str, help='user id needs to be passed to delete a user', required=True)
    update_parser.add_argument('-f', '--file-path', type=str, help='file contains user details', required=True)
    update_parser.add_argument('-d', '--domain', type=str, help='specify domain using --domain argument',
                               required=True)

    # delete command to delete a user
    delete_parser = subparsers.add_parser('delete', help='Delete a user')
    delete_parser.add_argument('--id', type=str, help='user id needs to be passed to delete a user', required=True)
    delete_parser.add_argument('-d', '--domain', type=str, help='specify domain using --domain argument',
                               required=True)

    # get command to retrieve a user
    get_parser = subparsers.add_parser('get', help='retrieve a user')
    get_parser.add_argument('--id', type=str, help='user id needs to be passed to retrieve a user', required=True)
    get_parser.add_argument('-d', '--domain', type=str, help='specify domain using --domain argument',
                            required=True)

    args = parser.parse_args()
    main(args)
