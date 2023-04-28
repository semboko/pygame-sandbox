
PGraphics pg;
int v1;
float speed;
JSONObject datas;
PVector[] lines1, lines2, circles1;
PVector player, offset;
boolean isdraw, isdrawc, isdel;
String last;
int circles;
int lines;

void setup() {
  lines1 = new PVector[200];
  lines2 = new PVector[200];
  isdel = false;
  circles1 = new PVector[200];
  last = "line";
  speed = 3;

  circles = 0;
  isdraw = false;
  isdrawc = false;
  lines = 0;
  size(1500, 500);
  noStroke();
  pg = createGraphics(width, height);
  player = new PVector(width/2, height/2);
  offset = new PVector();
}

void keyReleased() {
  if (key == 'z') isdel = false;
}
void draw() {

  pg.beginDraw();
  pg.background(255);
  if (keyPressed) {
    switch(key) {
    case 'e':
      datas = loadJSONObject("map.json");
      lines = 0;
      lines1 = new PVector[500];
      lines2 = new PVector[500];
      circles = 0;
      circles1 = new PVector[500];
      for (int i = 0; i < datas.getString("lines").split("\n").length; i += 1) {
        String strs = datas.getString("lines").split("\n")[i];
        String[] l = strs.split(" ");
        lines += 1;
        lines1[i] = new PVector(float(l[0]), float(l[1]));
        lines2[i] = new PVector(float(l[2]), float(l[3]));
      }
      for (int i = 0; i < datas.getString("circles").split("\n").length; i += 1) {
        String strs = datas.getString("circles").split("\n")[i];
        String[] l = strs.split(" ");
        circles += 1;
        circles1[i] = new PVector(float(l[0]), float(l[1]), float(l[2]));
      }
      String[] d = datas.getString("player").split(" ");
      player = new PVector(float(d[0]), float(d[1]));
      break;
    case 'p':
      player = new PVector(mouseX - offset.x, mouseY - offset.y);
      break;
    case 'r':
      lines = 0;
      lines1 = new PVector[200];
      lines2 = new PVector[200];
      circles = 0;
      circles1 = new PVector[200];
      break;
    case 'z':
      if (!isdel)
        if (last == "line") {
          lines -= 1;
          lines1[lines] = new PVector();
          lines2[lines] = new PVector();
        }
      if (last == "circle") {
        circles -= 1;
        circles1[lines] = new PVector();
      }
      isdel = true;
      break;
    case 'q':
      datas = new JSONObject();
      datas.setString("circles", "");
      datas.setString("lines", "");
      for (int i = 0; i < lines; i += 1) {
        String l = lines1[i].x + " " + lines1[i].y + " " + lines2[i].x + " " + lines2[i].y;
        datas.setString("lines", datas.getString("lines") + l + "\n");
      }
      for (int i = 0; i < circles; i += 1) {
        String l = circles1[i].x + " " + circles1[i].y + " " + circles1[i].z;
        datas.setString("circles", datas.getString("circles") + l + "\n");
      }
      datas.setString("player", player.x + " " + player.y);
      datas.setString("code", "");
      saveJSONObject(datas, "map.json");
      break;
    case 'w':
      offset.y += speed;
      break;
    case 'a':
      offset.x += speed;
      break;
    case 's':
      offset.y -= speed;
      break;
    case 'd':
      offset.x -= speed;
      break;
    case 'x':
      if (speed > 0)
      speed -= 1;
      break;
    case 'c':
      speed += 1;
      break;
    }
  }
  if (mouseButton == LEFT && !isdraw) {
    last = "line";
    lines1[lines] = new PVector(mouseX - offset.x, mouseY - offset.y);
    lines2[lines] = new PVector(mouseX - offset.x, mouseY - offset.y);
    lines += 1;
    isdraw = true;
  }
  if (mouseButton == LEFT && isdraw) {
    println(lines);
    // pg.line(lines1[lines-1].x, lines1[lines-1].y, lines2[lines-1].x, lines2[lines-1].y);
    lines2[lines-1] = new PVector(mouseX - offset.x, mouseY - offset.y);
  }
  if (!(mouseButton == LEFT) && isdraw) {
    isdraw = false;
  }
  if (mouseButton == RIGHT && !isdrawc) {
    isdrawc = true;
    last = "circle";
  }
  if (!(mouseButton == RIGHT) && isdrawc) {
    circles1[circles] = new PVector(mouseX - offset.x, mouseY - offset.y, 15);
    circles += 1;
    isdrawc = false;
  }
  for (int x = 0; x < lines; x += 1) {
    pg.stroke(0);
    // println(lines1[x].x, lines1[x].y, lines2[x].x, lines2[x].y);
    pg.line(lines1[x].x + offset.x, lines1[x].y + offset.y, lines2[x].x + offset.x, lines2[x].y + offset.y);
  }
  for (int x = 0; x < circles; x += 1) {
    pg.stroke(255, 0, 0);
    println(circles1[x]);
    pg.circle(circles1[x].x + offset.x, circles1[x].y + offset.y, circles1[x].z);
  }
  pg.rect(player.x + offset.x, player.y + offset.y, 50, 50);
  pg.endDraw();
  image(pg, 0, 0);
}
public void mouseWheel(MouseEvent me) {
  if (last == "circle") {
    if (me.getCount() < 0) {
      circles1[circles-1].z *= 0.9;
    } else {
      circles1[circles-1].z *= 1.1;
    }
  }
}
