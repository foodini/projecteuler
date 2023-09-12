#include <stdio.h>

int main() {
  FILE * out;

  out = fopen("0202_graph.ppm", "wb");
  int width = 5250;
  int height = 4000;
  int border = 100;
  int spacing = 100;
  int dot_size = 16;
  fprintf(out, "P6 %d %d 255\n", width, height);
  for(int y=0; y<height; y++) {
    int y_pos = height - border - y;
    for(int x=0; x<width; x++) {
      int x_pos = -border + x;
      if(x_pos < 0 || y_pos < 0 || y_pos > x_pos) {
        fputc(0xff, out);
        fputc(0xff, out);
        fputc(0xff, out);
      } else {
        if(x_pos % spacing < 2 || y_pos % spacing < 2 ||
           (x_pos + y_pos) % spacing < 3) {
          fputc(0x00, out);
          fputc(0x00, out);
          fputc(0x00, out);
        } else {
          int x_test = x_pos - y_pos + dot_size/2;
          int y_test = y_pos + dot_size/2;
          if(x_test > 0 &&
             x_test % (spacing*3) < dot_size &&
             y_test % (spacing) < dot_size) {
            fputc(0x00, out);
            fputc(0x00, out);
            fputc(0x00, out);
          } else {
            fputc(0xff, out);
            fputc(0xff, out);
            fputc(0xff, out);
          }
        }
      }
    }
  }
}
