from pyfcm import FCMNotification

def push_notification(token, msg):
    # api-key itu di dapat dari server key message clode
    push_service = FCMNotification(api_key="AAAAKbHd_U0:APA91bGMrrCC59haFV0pzfTqe6m5G0RKuN82PL9FtjBKoFqbEdo38vzujWZKgasSkBYsF1dNQFjkHapi2sdggfN_nlBOVR25XR9mZ4YyWtvQVqdsPc_CXad2LXvTMvll2_wVnQ1LX-0J")

    token_firebase = token
    title = "CAMART"

    action_push = push_service.notify_single_device(registration_id = token_firebase, message_title=title, message_body = msg)

    # push two device
    # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
    # print action_push