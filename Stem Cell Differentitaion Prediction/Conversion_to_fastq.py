from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import six_frame_translations
from tqdm import tqdm



def fastq_to_txt(fastq_file, txt_file):
    with open(fastq_file, "r") as infile, open(txt_file, "w") as outfile:
        for record in SeqIO.parse(infile, "fastq"):
            outfile.write(f"{record.seq}\n")

# Provide the path to your FASTQ file and the output TXT file
fastq_file = "./SRR20974333.fastq"
txt_file = "output.txt"

fastq_to_txt(fastq_file, txt_file)

# Step 1: Read a continuous RNA sequence from a TXT file
def read_rna_sequence(txt_file):
    with open(txt_file, "r") as file:
        sequence = file.read().strip()
    return sequence

# Step 2: Identify ORFs using six-frame translation (optional)
def identify_orfs(rna_sequence):
    return six_frame_translations(rna_sequence)

# Step 3: Find all ORFs in all three forward frames and select the longest
def find_longest_orf(rna_sequence):
    start_codon = 'AUG'
    stop_codons = ['UAA', 'UAG', 'UGA']
    longest_orf = Seq("")
    
    for frame in range(3):
        orf_start = None
        for i in tqdm(range(frame, len(rna_sequence), 3)):
            codon = rna_sequence[i:i+3]
            if codon == start_codon and orf_start is None:
                orf_start = i
            elif codon in stop_codons and orf_start is not None:
                orf = rna_sequence[orf_start:i+3]  # Include the stop codon
                if len(orf) > len(longest_orf):
                    longest_orf = orf
                orf_start = None
    return longest_orf

# Step 4: Translate the correct ORF
def translate_orf(orf):
    protein_sequence = orf.translate(to_stop=True)
    return protein_sequence

# Step 5: Main function to execute the steps and save the results
def main(input_file, output_file):
    rna_sequence = read_rna_sequence(input_file)
    if not rna_sequence:
        print("No sequence found in the file.")
        return
    
    orf_translation_output = []
    
    # Optionally identify ORFs for visualization
    orf_translation_output.append("Six-frame translations:")
    orf_translation_output.append(identify_orfs(rna_sequence))
    
    longest_orf = find_longest_orf(rna_sequence)
    if len(longest_orf) == 0:
        orf_translation_output.append("No ORF found.")
    else:
        protein_sequence = translate_orf(longest_orf)
        orf_translation_output.append(f"Longest ORF: {longest_orf}")
        orf_translation_output.append(f"Translated Protein Sequence: {protein_sequence}")
    
    with open(output_file, "w") as out_file:
        out_file.write("\n".join(orf_translation_output))

# Provide the path to your input RNA sequence TXT file and the output TXT file
output_file = "./protein_sequences.txt"
input_file = "./output.txt"
main(input_file, output_file)