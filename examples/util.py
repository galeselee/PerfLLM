
def example_parser_arg(parser):
    parser.add_argument('--datafile', type=str, 
                        help="The path of the datafile",
                        default=None)
    parser.add_argument('--enable_token_num', type=bool, 
                        help="enable the token num of input and output or not",
                        default=False)
    parser.add_argument('--model', type=str, 
                        help="The path of the tokenizer used for token number counting if enable the token num",
                        default=None)
    parser.add_argument('--seed', type=int, 
                        help="The random seed for database",
                        default=0)
    parser.add_argument("--server_port", type=int,
                        help="The port of server, default is 8000")