print("Subscribers package initialized")


from subscribers.updateUsernameSubscriber import start_kafka_consumer

from subscribers.UpdateProductQuantitySubscriber import start_price_updated_consumer

from subscribers.UpdateProductQuantitySubscriber import consume_product_price_updated_event

from subscribers.updateUsernameSubscriber import consume_username_updated_event