
  PGraphics pg;
  int v1;
  JSONObject datas;
  PVector[] lines1;
  PVector[] lines2;
  PVector[] circles1;
  PVector player;
  boolean isdraw;
  boolean isdrawc;
  String last;
  int circles;
  int lines;
  
  void setup() {
    lines1 = new PVector[200];
    lines2 = new PVector[200];
    circles1 = new PVector[200];
    player = new PVector(250, 250);
    last = "line";
    
    circles = 0;
    isdraw = false;
    isdrawc = false;
    lines = 0;
    size(640, 360);  
    noStroke();
    pg = createGraphics(640, 360);
  }
  
  void draw() {

    pg.beginDraw();
    pg.background(255);
    if (mouseButton == LEFT && !isdraw) {
      last = "line";
      lines1[lines] = new PVector(mouseX, mouseY);
      lines2[lines] = new PVector(mouseX, mouseY);
      lines += 1;
      isdraw = true;
    }
    if (mouseButton == LEFT && isdraw) {
      println(lines);
      // pg.line(lines1[lines-1].x, lines1[lines-1].y, lines2[lines-1].x, lines2[lines-1].y);
      lines2[lines-1] = new PVector(mouseX, mouseY);
    }
    if (!(mouseButton == LEFT) && isdraw) {
      isdraw = false;
    }
    if (mouseButton == RIGHT && !isdrawc) {
      isdrawc = true;
      last = "circle";
    }
    if (!(mouseButton == RIGHT) && isdrawc) {
      circles1[circles] = new PVector(mouseX, mouseY, 15);
      circles += 1;
      isdrawc = false;
    }
    for (int x = 0; x < lines; x += 1) {
      pg.stroke(0);
      println(lines1[x].x, lines1[x].y, lines2[x].x, lines2[x].y);
      pg.line(lines1[x].x, lines1[x].y, lines2[x].x, lines2[x].y);
    }
    for (int x = 0; x < circles; x += 1) {
      pg.stroke(255, 0, 0);
      println(circles1[x]);
      pg.circle(circles1[x].x, circles1[x].y, circles1[x].z);
    }
    pg.rect(player.x, player.y, 25, 25);
    pg.endDraw();
    image(pg, 0, 0);
  }
 void keyPressed() {
  if (key == 'e') {
    datas = loadJSONObject("map.json");
    lines = 0;
    lines1 = new PVector[200];
    lines2 = new PVector[200];
    circles = 0;
    circles1 = new PVector[200];
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
  }
  // if (key == 's') {
  //   String[] slines = loadStrings("map.txt");
  //   lines1 = new PVector[200];
  //   lines2 = new PVector[200];
     
  //   for (int i = 0; i < slines.length; i += 1) {
  //     if (slines[i] == "") break;
  //     float[] s1lines = float(split(slines[i], ' '));
  //     // println(s1lines);
  //     // if (s1lines[i] == null) break;
       
  //     lines1[i] = new PVector(s1lines[0], s1lines[1]);
  //     lines2[i] = new PVector(s1lines[2], s1lines[3]);
  //   }
  //   lines = slines.length;
     
  //   String[] sballs = loadStrings("map_circles.txt");
  //   // println(sballs);
  //   circles1 = new PVector[200];
  //   for (int i = 0; i < slines.length; i += 1) {
  //     if (sballs[i] == "") break;
  //     float[] s1balls = float(split(sballs[i], ' '));
  //     // println(s1lines);
  //     // if (s1lines[i] == null) break;
  //     circles1[i] = new PVector(s1balls[0], s1balls[1], s1balls[2]);
  //   }
  //     circles = sballs.length-1;
     
  //}
   if (key == 'p') {
    player = new PVector(mouseX, mouseY);
   }
   if (key == 'r') {
    lines = 0;
    lines1 = new PVector[200];
    lines2 = new PVector[200];
    circles = 0;
    circles1 = new PVector[200];
  }
  if (key == 'z') {
    if (last == "line") {
      lines -= 1;
      lines1[lines] = new PVector();
      lines2[lines] = new PVector();
    }
    if (last == "circle") {
      circles -= 1;
      circles1[lines] = new PVector();
    }
  }
  if (key == 'q') {
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
    //for (int i = 0; i < lines; i += 1) {
    //  datas[i] = lines1[i].x + " " + lines1[i].y + " " + lines2[i].x + " " + lines2[i].y;
    //}
    //saveStrings("map.txt", datas);
    //String[] datas_circles = new String[circles];
    //for (int i = 0; i < circles; i += 1) {
    //  datas_circles[i] = circles1[i].x + " " + circles1[i].y + " " + circles1[i].z;
    //}
    //saveStrings("map_circles.txt", datas_circles);
    //String[] player_data = {player.x + " " + player.y};
    //saveStrings("map_player.txt", player_data);
    //// exit();
  }
 }
  public void mouseWheel(MouseEvent me) {
     if (last == "circle") {
       if (me.getCount() < 0) {
         circles1[circles-1].z *= 0.9;
       }
       else {
         circles1[circles-1].z *= 1.1;
       }
     }
  }
