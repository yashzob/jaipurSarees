from django_rq import get_queue
from .models import Product

def enqueue_update(product_id, data):
    """
    Enqueue a product update to be processed later
    Args:
        product_id: ID of product to update
        data: Dictionary of fields to update
    Returns:
        RQ Job ID
    """
    queue = get_queue('default')
    return queue.enqueue(
        process_update, 
        product_id,
        data,
        result_ttl=86400  # Keep results for 24 hours
    )

def process_update(product_id, data):
    """
    Process a queued product update
    Args:
        product_id: ID of product to update
        data: Dictionary of fields to update
    Returns:
        True if successful, error message if failed
    """
    try:
        product = Product.objects.get(pk=product_id)
        for field, value in data.items():
            setattr(product, field, value)
        product.save()
        return True
    except Product.DoesNotExist:
        return "Product not found"
    except Exception as e:
        return str(e)
