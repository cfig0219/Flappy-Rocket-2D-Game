#include <fstream>
#include <iostream>

int main() {
  std::ifstream imageFile("Photos/Earth_lowRes.png", std::ios::binary);

  if (!imageFile) {
    std::cout << "Failed to open image file" << std::endl;
    return 1;
  }

  // Get size of file
  imageFile.seekg(0, std::ios::end); 
  std::streampos fileSize = imageFile.tellg();
  imageFile.seekg(0, std::ios::beg);

  // Read file data into buffer
  char * buffer = new char[fileSize];
  imageFile.read(buffer, fileSize);

  // Render buffer data to screen
  // ...

  delete[] buffer;
  return 0;
}
