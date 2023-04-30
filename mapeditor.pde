import controlP5.*;

ControlP5 cp5;
PGraphics pg;
int v1;
float speed;
JSONObject datas;
PVector[] lines1, lines2, circles1, blocks, pj1, pj2;
PVector player, offset, maplv;
boolean isdraw, isdrawc, isdel, terrain, b1, b2, b3, isdrawb, isdrawp;
String last, mode, mapl;
String[] modes;
int circles, modr, blockr;
int lines, pj;

void setup() {
  isdel = false;
  last = "line";
  mode = "line";
  isdrawb = false;
  isdrawp = false;
  modes = new String[6];
  modes[0] = "line";
  modes[1] = "circle";
  modes[2] = "player";
  modes[3] = "Terrain Block";
  modes[4] = "Pj";
  modes[5] = "loadmap";
  b1 = false;
  b2 = false;
  b3 = false;

  modr = 0;
  speed = 3;
  restart();
  isdraw = false;
  isdrawc = false;
  lines = 0;
  pj = 0;
  size(1500, 500);
  noStroke();
  pg = createGraphics(width, height);
  player = new PVector(width/2, height/2);
  offset = new PVector();
  cp5 = new ControlP5(this);
  cp5.addButton("terrain")
    .setValue(1)
    .setSize(50, 19)
    ;
  cp5.addTextlabel("ttt")
    .setText("Terrain ON")
    .setPosition(100, 50)
    .setColorValue(#37678B)
    .setFont(createFont("Georgia", 20))
    ;
  cp5.addTextlabel("M")
    .setText("mode: line")
    .setPosition(250, 50)
    .setColorValue(#37678B)
    .setFont(createFont("Georgia", 20))
    ;
  cp5.addButton("up")
    .setValue(1)
    .setPosition(10, 160)
    .setSize(50, 19)
    ;
  cp5.addButton("down")
    .setValue(1)
    .setPosition(10, 190)
    .setSize(50, 19)
    ;
  cp5.addButton("restart")
    .setValue(1)
    .setPosition(70, 160)
    .setSize(50, 19)
    ;
  cp5.addTextfield("mapload")
    .setPosition(200, 160)
    .setSize(150, 19)
    ;
}
void restart() {
  lines = 0;
  lines1 = new PVector[600];
  lines2 = new PVector[600];
  pj1 = new PVector[600];
  pj2 = new PVector[600];
  maplv = new PVector(0, 0);
  mapl = "";
  pj = 0;
  circles = 0;
  circles1 = new PVector[600];
  blocks = new PVector[600];
  blockr = 0;
}
void keyReleased() {
  if (key == 'z') isdel = false;
}
void draw() {

  pg.beginDraw();
  pg.background(255);
  if ((mouseX < 350 && mouseY < 160 + 19) && (mouseX > 200 && mouseY > 160)) {
    return;
  }
  if (terrain) cp5.get(Textlabel.class, "ttt").setText("Terrain ON");
  else cp5.get(Textlabel.class, "ttt").setText("Terrain OFF");
  terrain = cp5.get(Button.class, "terrain").isOn();
  if (cp5.get(Button.class, "restart").isOn() != b3) {
    restart();
  }
  if (cp5.get(Button.class, "up").isOn() != b1) {
    b1 = !b1;
    if (modr > 0) modr -= 1;
    mode = modes[modr];
  }
  if (cp5.get(Button.class, "down").isOn() != b2) {
    b2 = !b2;
    if (modr < 5) modr += 1;
    mode = modes[modr];
  }
  cp5.get(Textlabel.class, "M").setText("mode: " + mode);
  // println(mouseX, mouseY);
  if (keyPressed) {
    switch(key) {
    case 'e':
      datas = loadJSONObject("map.json");
      terrain = datas.getBoolean("terrain");
      restart();
      for (int i = 0; i < datas.getString("lines").split("\n").length; i += 1) {
        String strs = datas.getString("lines").split("\n")[i];
        String[] l = strs.split(" ");
        lines += 1;
        lines1[i] = new PVector(float(l[0]), float(l[1]));
        lines2[i] = new PVector(float(l[2]), float(l[3]));
      }
      for (int i = 0; i < datas.getString("pj").split("\n").length; i += 1) {
        String strs = datas.getString("pj").split("\n")[i];
        String[] l = strs.split(" ");
        pj += 1;
        pj1[i] = new PVector(float(l[0]), float(l[1]));
        pj2[i] = new PVector(float(l[2]), float(l[3]));
      }
      for (int i = 0; i < datas.getString("circles").split("\n").length; i += 1) {
        String strs = datas.getString("circles").split("\n")[i];
        String[] l = strs.split(" ");
        circles += 1;
        circles1[i] = new PVector(float(l[0]), float(l[1]), float(l[2]));
      }
      for (int i = 0; i < datas.getString("blocks").split("\n").length; i += 1) {
        String strs = datas.getString("blocks").split("\n")[i];
        String[] l = strs.split(" ");
        blockr += 1;
        if (strs.length() == 0) {
          blockr = 0;
          break;
        }
        blocks[i] = new PVector(float(l[0]), float(l[1]));
      }
      String[] d = datas.getString("player").split(" ");
      player = new PVector(float(d[0]), float(d[1]));
      d = datas.getString("mlv").split(" ");
      maplv = new PVector(float(d[0]), float(d[1]));
      mapl = datas.getString("ml");
      break;
    case 'r':
      restart();
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
      datas.setString("pj", "");
      datas.setString("ml", "");
      datas.setString("mlv", "");
      datas.setString("blocks", "");
      datas.setBoolean("terrain", terrain);
      for (int i = 0; i < lines; i += 1) {
        String l = lines1[i].x + " " + lines1[i].y + " " + lines2[i].x + " " + lines2[i].y;
        datas.setString("lines", datas.getString("lines") + l + "\n");
      }
      for (int i = 0; i < pj; i += 1) {
        String l = pj1[i].x + " " + pj1[i].y + " " + pj2[i].x + " " + pj2[i].y;
        datas.setString("pj", datas.getString("pj") + l + "\n");
      }
      for (int i = 0; i < circles; i += 1) {
        String l = circles1[i].x + " " + circles1[i].y + " " + circles1[i].z;
        datas.setString("circles", datas.getString("circles") + l + "\n");
      }
      for (int i = 0; i < blockr; i += 1) {
        String l = blocks[i].x + " " + blocks[i].y;
        datas.setString("blocks", datas.getString("blocks") + l + "\n");
      }
      datas.setString("player", player.x + " " + player.y);
      datas.setString("ml", mapl);
      datas.setString("mlv", maplv.x + " " + maplv.y);
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
  if (!(mouseX < 50 + 10 + 80 && mouseY < 200)) {
    switch (mode) {
    case "line":
      if (mouseButton == LEFT && !isdraw) {
        last = "line";
        lines1[lines] = new PVector(mouseX - offset.x, mouseY - offset.y);
        lines2[lines] = new PVector(mouseX - offset.x, mouseY - offset.y);
        lines += 1;
        isdraw = true;
      }
      if (mouseButton == LEFT && isdraw) {
        //println(lines);
        // pg.line(lines1[lines-1].x, lines1[lines-1].y, lines2[lines-1].x, lines2[lines-1].y);
        lines2[lines-1] = new PVector(mouseX - offset.x, mouseY - offset.y);
      }
      if (!(mouseButton == LEFT) && isdraw) {
        isdraw = false;
      }
      break;
    case "Pj":
      if (mouseButton == LEFT && !isdrawp) {
        last = "pj";
        pj1[pj] = new PVector(mouseX - offset.x, mouseY - offset.y);
        pj2[pj] = new PVector(mouseX - offset.x, mouseY - offset.y);
        pj += 1;
        isdrawp = true;
      }
      if (mouseButton == LEFT && isdrawp) {
        //println(lines);
        // pg.line(lines1[lines-1].x, lines1[lines-1].y, lines2[lines-1].x, lines2[lines-1].y);
        pj2[pj-1] = new PVector(mouseX - offset.x, mouseY - offset.y);
      }
      if (!(mouseButton == LEFT) && isdrawp) {
        isdrawp = false;
      }
      break;
    case "circle":
      if (mouseButton == LEFT && !isdrawc) {
        isdrawc = true;
        last = "circle";
      }
      if (!(mouseButton == LEFT) && isdrawc) {
        circles1[circles] = new PVector(mouseX - offset.x, mouseY - offset.y, 15);
        circles += 1;
        isdrawc = false;
      }
      break;
    case "player":
      if (mouseButton == LEFT)
        player = new PVector(mouseX - offset.x, mouseY - offset.y);
      break;
    case "Terrain Block":
      if (mouseButton == LEFT && !isdrawb) {
        float x = mouseX - offset.x;
        float y = mouseY - offset.y;

        blocks[blockr] = new PVector(x - x % 25, y - y % 25);
        blockr += 1;
        isdrawb = true;
      }
      if (!(mouseButton == LEFT) && isdrawb) {
        isdrawb = false;
      }
      break;
    case "loadmap":
      if (mouseButton == LEFT) {
        mapl = cp5.get(Textfield.class, "mapload").getText();
        maplv = new PVector(mouseX - offset.x, mouseY - offset.y);
      }
      break;
    }
  }
  for (int x = 0; x < lines; x += 1) {
    pg.stroke(0);
    // println(lines1[x].x, lines1[x].y, lines2[x].x, lines2[x].y);
    pg.line(lines1[x].x + offset.x, lines1[x].y + offset.y, lines2[x].x + offset.x, lines2[x].y + offset.y);
  }
  for (int x = 0; x < pj; x += 1) {
    pg.stroke(0, 100, 255);
    // println(lines1[x].x, lines1[x].y, lines2[x].x, lines2[x].y);
    pg.line(pj1[x].x + offset.x, pj1[x].y + offset.y, pj2[x].x + offset.x, pj2[x].y + offset.y);
  }
  for (int x = 0; x < blockr; x += 1) {
    pg.stroke(0);
    // println(lines1[x].x, lines1[x].y, lines2[x].x, lines2[x].y);
    pg.rect(blocks[x].x + offset.x, blocks[x].y + offset.y, 25, 25);
  }
  for (int x = 0; x < circles; x += 1) {
    pg.stroke(255, 0, 0);
    //println(circles1[x]);
    pg.circle(circles1[x].x + offset.x, circles1[x].y + offset.y, circles1[x].z);
  }
  pg.stroke(185, 100, 0);
  pg.rect(player.x + offset.x, player.y + offset.y, 50, 50);
  pg.rect(maplv.x + offset.x, maplv.y + offset.y, 60, 60);
  pg.stroke(0);
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
