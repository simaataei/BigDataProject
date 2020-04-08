import os

e_values = {1: 10, 2: 1, 3: 0.1, 4: 0.01, 5: 0.001, 6: 0.0001, 7: 0.00001, 8: 0.000001, 9: 0.0000001, 10: 0.00000001,
            11: 0.000000001, 12: 0.0000000001}

for fold in range(1, 6):
    for e_value in e_values:
        cmd = f"blastp -query ../Selected30_subfamilies_test_tcdb_fold_{fold}.fasta -db ../DB_Selected30_subfamilies_train_tcdb_fold_{fold} -outfmt '6 std qlen slen' -out output_test_on_train_subfamilies_fold_{fold}_{e_value}.list -evalue {e_values[e_value]}"
        os.system(cmd)
