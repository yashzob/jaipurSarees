from django.db import migrations, connection

def create_trigger_for_postgres(apps, schema_editor):
    if connection.vendor != 'postgresql':
        return  # Skip if not PostgreSQL

    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE OR REPLACE FUNCTION update_product_stock()
            RETURNS TRIGGER AS $$
            BEGIN
                IF TG_OP = 'UPDATE' THEN
                    UPDATE store_product
                    SET stock = stock - (NEW.quantity - OLD.quantity)
                    WHERE id = NEW.product_id;
                ELSIF TG_OP = 'INSERT' THEN
                    UPDATE store_product
                    SET stock = stock - NEW.quantity
                    WHERE id = NEW.product_id;
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)

        cursor.execute("""
            DROP TRIGGER IF EXISTS reduce_stock_trigger ON store_orderitem;
            CREATE TRIGGER reduce_stock_trigger
            AFTER INSERT OR UPDATE ON store_orderitem
            FOR EACH ROW
            EXECUTE FUNCTION update_product_stock();
        """)

def remove_trigger_for_postgres(apps, schema_editor):
    if connection.vendor != 'postgresql':
        return

    with connection.cursor() as cursor:
        cursor.execute("DROP TRIGGER IF EXISTS reduce_stock_trigger ON store_orderitem;")
        cursor.execute("DROP FUNCTION IF EXISTS update_product_stock();")

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20250409_2209'),  # <- replace with actual previous migration name
    ]

    operations = [
        migrations.RunPython(create_trigger_for_postgres, reverse_code=remove_trigger_for_postgres),
    ]
