import argparse


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description="""
        This is a Command line interface """)

    my_parser.add_argument('--nb_pages', help='number of pages to scrap', type=int, required=False)
    my_parser.add_argument('--Product_Table', help='Scrap Product Table', type=bool, required=False)
    my_parser.add_argument('--Product_Spec_Table', help='Scrap Product Spec Title', type=bool, required=False)
    my_parser.add_argument('--Supplier_Table', help='Scrap Supplier Table', type=bool, required=False)

    args = my_parser.parse_args()

    if args.Product_Table == True:
        is_titles = True
        is_delivery = True
        is_qty_sold = True
        is_ratings = True
        is_stores = True
        is_discounts = True

    if args.Product_Spec_Table == True:
        is_nb_followers = True
        is_name = True
        is_store_no = True
        is_supplier_country = True
        is_opening_date = True

    if args.Product_Spec_Table == True:
        is_brand_name = True
        is_video_memory_capacity = True
        is_interface_type = True
        is_stream_processors = True
        is_chip_process = True
        is_model_number = True
        is_pixel_pipelines = True
        is_launch_date = True
        is_output_interface_type1 = True
        is_output_interface_type2 = True
        is_memory_interface = True
