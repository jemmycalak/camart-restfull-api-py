from pyfcm import FCMNotification

def push_notification(token, msg):
    # api-key itu di dapat dari server key message clode
    push_service = FCMNotification(api_key="AAAApd2iFkc:APA91bG42kA4o-uQpkveeZxQu6Y3527xd8sRrLTwgq6xvz7fqIeseig-yBsGi8UAXnzjDEmymQrJm2hDU7Nt7YP7VMjajBnZ4eW9lt0tCkYAiHX_n-3KZKB5dbPwsblWJonqPSrMtISn")

    token_firebase = token
    title = "CAMART"

    action_push = push_service.notify_single_device(registration_id = token_firebase, message_title=title, message_body = msg)

    # push two device
    # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
    # print action_push