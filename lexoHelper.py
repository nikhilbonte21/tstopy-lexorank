def array_copy(source_array, source_index, destination_array, destination_index, length):
    destination = destination_index
    final_length = source_index + length
    for i in range(source_index, final_length):
        destination_array[destination] = source_array[i]
        destination += 1

lexo_helper = {
    'array_copy': array_copy
}
