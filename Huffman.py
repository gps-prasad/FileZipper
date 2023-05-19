import heapq
import os

class BinaryTree:
    def __init__(self,value,frequ):
        self.value = value
        self.frequ = frequ
        self.left = None
        self.right = None
        
    def __lt__(self,other):
        return self.frequ < other.frequ
    
    def __eq__(self,other):
        return self.frequ == other.frequ        

class Huffmancode:
    
    def __init__(self,path):
        self.path = path
        self.heap = []
        self.code = {}
        self.reversecode = {}
        
    def frequency_from_text(self,text):
        frequ_dict = {}
        for char in text:
            if char not in frequ_dict:
                frequ_dict[char] = 0
            frequ_dict[char] +=1
        return frequ_dict    
    
    def Build_heap(self,frequency_dict):
        for key in frequency_dict:
            frequency = frequency_dict[key]
            binary_tree_node = BinaryTree(key,frequency)
            heapq.heappush(self.heap , binary_tree_node)
    
    def Build_Binary_Tree(self):
        while len(self.heap) > 1:
            binary_tree_node_1 = heapq.heappop(self.heap)
            binary_tree_node_2 = heapq.heappop(self.heap)
            sum_of_freq = binary_tree_node_1.frequ + binary_tree_node_2.frequ
            newnode = BinaryTree(None,sum_of_freq)
            newnode.left = binary_tree_node_1
            newnode.right = binary_tree_node_2
            heapq.heappush(self.heap,newnode)
        return
    def Build_Tree_Code_Helper(self,root,curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.code[root.value] = curr_bits
            self.reversecode[curr_bits] = root.value
            return
        self.Build_Tree_Code_Helper(root.left,curr_bits+'0')
        self.Build_Tree_Code_Helper(root.right,curr_bits+'1')
    
    def Build_Tree_Code(self):
        root = heapq.heappop(self.heap)
        self.Build_Tree_Code_Helper(root,'')
        

    def Build_Encoded_Text(self,text):
        encoded_text = ''
        for char in text:
            encoded_text += self.code[char]
            
        return encoded_text  
    
    
    def Build_Padded_Text(self,encoded_text):
        padding_value = 8 - (len(encoded_text) % 8)
        for i in range(padding_value):
            encoded_text += '0'
            
        padded_info = "{0:08b}".format(padding_value)
        padded_encoded_text = padded_info + encoded_text
        return padded_encoded_text
    
    def Build_Byte_Array(self, padded_text):
        array = []
        for i in range(0,len(padded_text) , 8):
            byte = padded_text[i:i+8]
            array.append(int(byte,2))
        return array    
    
    def compression(self):
        
        #To access the file and extract text from that file.
        filename,file_extension = os.path.splitext(self.path)
        output_path = filename + '.bin'
        with open (self.path,'r+') as file , open(output_path,'wb') as output:
            text = file.read()
            text = text.rstrip()
            
            frequency_dict = self.frequency_from_text(text)

            #Calculate frequency of each text and store it in freq. dictionary

            build_heap = self.Build_heap(frequency_dict)

            # Min heap for two minimum frquency.

            #Construct binary tree from Heap .

            self.Build_Binary_Tree()

            #construct code from binary tree and stored it in dictionary.

            self.Build_Tree_Code()

            #Construct encoded text.

            encoded_text = self.Build_Encoded_Text(text)

            #padding of text

            padded_text = self.Build_Padded_Text(encoded_text)

            #We have to return that binary file as an output.

            bytes_array = self.Build_Byte_Array(padded_text)

            final_bytes = bytes(bytes_array)
            output.write(final_bytes)
        print("Compressed")
        return output_path
    
    def Remove_Padding(self,text):
        padded_info = text[:8]
        extra_padding = int(padded_info,2)
        text = text[8:]
        padding_removed_text = text[:-1*extra_padding]
        return padding_removed_text
        
    def Decompress_Text(self,text):    
        decoded_text = ''
        current_bits = ''
        for bit in text:
            current_bits += bit
            if current_bits in self.reversecode:
                character = self.reversecode[current_bits]
                decoded_text += character
                current_bits = ""
        return decoded_text
    
    
    def decompress(self,input_path):
        filename,file_extension = os.path.splitext(input_path)
        output_path = filename + '_decompressed' + '.txt'
        with open(input_path,'rb') as file , open(output_path,'w') as output:
            bit_string = ''
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8,'0')
                bit_string += bits
                byte = file.read(1)
                
            actual_text = self.Remove_Padding(bit_string)    
            decompressed_text = self.Decompress_Text(actual_text)
            output.write(decompressed_text)
        return    
            
path = input('Enter the file path -> ')  
h = Huffmancode(path)
output_path = h.compression()
#h.decompress(output_path)