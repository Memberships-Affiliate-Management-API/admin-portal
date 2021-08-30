
self.addEventListener('load', () => {
    console.log("loaded app")

    let token_sent = false;
    let incoming_notifications_messages = [];

    // Dispatch messages to service worker
    let send_auth_to_service_worker = async (message )=> {
        navigator.serviceWorker.ready.then(registration => {
            registration.active.postMessage({
                type: "auth-token",
                token: message
            });
        });
        return true;
    };

    let dispatch_messages = async (message, type) => {
        navigator.serviceWorker.ready.then(registration => {
            registration.active.postMessage({
                type: type,
                message: message
            });
        });
        return true;
    }

    let handle_auth_token_messages = message => {
        switch(message){
            case "Token-Received": token_sent = true; break;
            case "Not-Logged-IN": token_sent = false;break;
            default:  break;
        }
    };


    let handle_auth_token_expired = message => {
        // TODO remove token from local-storage
        // send user to login and inform user the token has expired
        localStorage.removeItem('x-access-token');
        token_sent = false;
        document.location = "/logout";
        console.log('User logged out authorization expired')
    };

    let handle_auth_status_messages = ({ type,status, token}) => {
        // the intent to sign-in/out is received continue signing-out/in
        if (status === "logged-out") {
            localStorage.removeItem('x-access-token');
            if (document.location.href.endsWith("/logout")){document.location = "/"}
        }
        console.log("location href: ", document.location.href)
        if ((status === "logged-in")){
            localStorage.setItem('x-access-token',token)
        }
    }

    let handle_user_messages = (data) => {
        switch (data.status){
            case "counted": {
                localStorage.setItem('visitors', data.unique_visitors)
                localStorage.setItem('return_visitors', data.return_visitors)
                localStorage.setItem('counted', 'yes')
            }break;
            case "page-view":{
                localStorage.setItem('page_views', data.page_views )
            }break;
            default: break;
        }
    }

    // Listen to messages from service worker;
    let message_listener = e => {
        console.log("Service Worker sent me a message back : ", e.data);
        // call different handlers depending on the message being sent
        switch(e.data.type){
        case "auth-token": handle_auth_token_messages(e.data.message); break;
        case "auth-token-expired": handle_auth_token_expired(e.data.message); break;
        case "notification-message": handle_notification_message(e.data.message);break;
        case "auth-status": handle_auth_status_messages(e.data);break;
        case "user-messages": handle_user_messages(e.data);break;
        default : break;
        }
        // re run notification module
        // notifications.init();
    };

    let service_registration = async function(){
        console.log("trying to register service worker")
        let registered = await navigator.serviceWorker.register('sw.js');
        navigator.serviceWorker.addEventListener('message', message_listener);
        console.log('register service worker')
        return registered;
    }

    self.addEventListener('message', e => {
        console.log('Message sent from somewhere else',e);
    })

    // initialize login on first load
    let init_auth_token_send = async function(){
        let token = localStorage.getItem('x-access-token');
        // console.log("checking token : ", token);
        if ((token !== "undefined") && (token !== "") && (token !== null) && (token !== "null")){
            if (!token_sent){
                send_auth_to_service_worker(token).then(() => {})
            }
        }
        return true;
    };

    let unique_visitor_send = async function(){
        await dispatch_messages({
            type: 'user-messages',status: 'count-unique',
        })
        return true;
    }
    let return_visitor_send = async function(){
        await dispatch_messages({
            type: 'user-messages',status: 'count-return',
        })
        return true;
    }
    let page_view_send = async function(){
        await dispatch_messages({
            type: 'user-messages', status: 'page-view'
        })
    }

    // ************************************************************************************//
    //  Notification Services
    let handle_notification_message = message => {
        // TODO- get hold of the header notification tab
        // TODO- send notification to header file
        incoming_notifications_messages.push(message);
    };

    service_registration().then(registered => {
        console.log("registering service worker")
        if (registered){
            init_auth_token_send().then(() => {
                // NOTE: initializing notification messaging
                console.log("service worker installed and auth initialized")
            })
        }
    });
})