import argparse


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description="""
        This is a Command line interface """)

    my_parser.add_argument('--nb_pages', help='number of pages to scrap', type=int, required=False)
    my_parser.add_argument('--is_titles', help='Product Title', type=bool, required=False)
    my_parser.add_argument('--is_delivery', help='Product delivery', type=bool, required=False)
    my_parser.add_argument('--is_qty_sold', help='Product quantity sold', type=bool, required=False)
    my_parser.add_argument('--is_ratings', help='Product rating', type=bool, required=False)
    my_parser.add_argument('--is_stores', help='Product sold at stores', type=bool, required=False)
    my_parser.add_argument('--is_discounts', help='Product discount', type=bool, required=False)
    my_parser.add_argument('--is_nb_followers', help='supplier number of followers', type=bool, required=False)
    my_parser.add_argument('--is_name', help='supplier name', type=bool, required=False)
    my_parser.add_argument('--is_store_no', help='supplier store', type=bool, required=False)
    my_parser.add_argument('--is_supplier_country', help='supplier country', type=bool, required=False)
    my_parser.add_argument('--is_opening_date', help='supplier opening date', type=bool, required=False)
    my_parser.add_argument('--is_brand_name', help='GPU brand number', type=bool, required=False)
    my_parser.add_argument('--is_video_memory_capacity', help='GPU video memory capacity', type=bool, required=False)
    my_parser.add_argument('--is_interface_type', help='GPU interface type', type=bool, required=False)
    my_parser.add_argument('--is_cooler_type', help='GPU color type', type=bool, required=False)
    my_parser.add_argument('--is_stream_processors', help='GPU stream processors', type=bool, required=False)
    my_parser.add_argument('--is_chip_process', help='GPU chip process', type=bool, required=False)
    my_parser.add_argument('--is_model_number', help='GPU model', type=bool, required=False)
    my_parser.add_argument('--is_pixel_pipelines', help='GPU pixel pipelines', type=bool, required=False)
    my_parser.add_argument('--is_launch_date', help='GPU launch date', type=bool, required=False)
    my_parser.add_argument('--is_output_interface_type1', help='GPU output interface1', type=bool, required=False)
    my_parser.add_argument('--is_output_interface_type2', help='GPU output interface2', type=bool, required=False)
    my_parser.add_argument('--is_memory_interface', help='GPU memory_interface', type=bool, required=False)

    args = my_parser.parse_args()
    print(args)
