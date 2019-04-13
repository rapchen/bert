class Params(object):

    def __init__(self):
        self.task_name = "TALE"
        self.data_dir = "D:/crw/out/blacktale1_2_1/tmp/"
        self.bert_config_file = "D:/crw/chinese_L-12_H-768_A-12/bert_config.json"
        self.vocab_file = "D:/crw/chinese_L-12_H-768_A-12/vocab.txt"
        self.output_dir = "D:/crw/out/blacktale1_2_1/tmp/"
        self.init_checkpoint = "D:/crw/out/blacktale1_2_1/model.ckpt-87"
        self.do_lower_case = True
        self.max_seq_length = 64
        self.do_train = False
        self.do_eval = False
        self.do_predict = True
        self.train_batch_size = 32
        self.eval_batch_size = 8
        self.predict_batch_size = 1

        # useless configs
        self.save_checkpoints_steps = 1000
        self.learning_rate = 2e-5
        self.use_tpu = False
        self.master = None
        self.iterations_per_loop = 1
        self.num_tpu_cores = 1

