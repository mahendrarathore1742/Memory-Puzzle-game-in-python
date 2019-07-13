import random,pygame,sys;
from pygame.locals import *;

FPS=30;
WINDOWWITDTH=640;
WINDOWHEIGHT=480;
REVELASPEED=1;
BOXSIZE=40;
GAPSIZE=10;
BORDERWIDTH=10;
BORDRHEIGHT=7;
GAME_SOUND={};


assert(BORDERWIDTH*BORDRHEIGHT)%2==0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN=int((WINDOWWITDTH-(BORDERWIDTH*(BOXSIZE+GAPSIZE)))/2);
YMARGIN=int((WINDOWHEIGHT-(BORDRHEIGHT*(BOXSIZE+GAPSIZE)))/2);

#             R    G  B
GRAY        =(100,100,100);
NAVYBLUE    =(60,60,100);
WHITE       =(255,255,255);
RED         =(255,0,0);
GREEN       =(0,255,0);
BLUE        =(0,0,255);
YELLOW      =(255,255,0);
ORANGE      =(255,128,0);
PURPLE      =(255,0,255);
CYAN        = (0,255,255);

BGCOLOR=NAVYBLUE;
LIGHTBGCOLOR=GRAY;
BOXCOLOR=WHITE;
HIGHLIGHTCOLOR=BLUE;

DOUNT='dount';
SQUARE='square';
DIAMOND='diamond';
LINSE='linse';
OVAL='oval';

ALLCOLOR=(RED,GREEN,BLUE,YELLOW,ORANGE,PURPLE,CYAN);
ALLSHAPES=(DOUNT,SQUARE,DIAMOND,LINSE,OVAL);
assert len(ALLCOLOR)*len(ALLSHAPES)*2>=BORDERWIDTH*BORDRHEIGHT;

def main():
    global FPSCLOCK,DISPLAYSURF;
    pygame.init();
    FPSCLOCK=pygame.time.Clock();
    DISPLAYSURF=pygame.display.set_mode((WINDOWWITDTH,WINDOWHEIGHT));

    mousex=0;
    mousey=0;
    pygame.display.set_caption('Memory puzzle');

    mainbord=getRabdomizedBoed();
    revealedBoxes=generateReveledBoxesData(False);

    firstSelecetion=None;

    DISPLAYSURF.fill(BGCOLOR);
    startGameAnimation(mainbord);

    while True:
        #this is main game loop
        mouseClicked=False;
        DISPLAYSURF.fill(BGCOLOR);
        drawBordr(mainbord,revealedBoxes);

        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYUP and event.key==K_ESCAPE):
                pygame.quit();
                sys.exit();

            elif event.type==MOUSEMOTION:
                mousex,mousey=event.pos;
            elif event.type==MOUSEBUTTONUP:
                mousex,mousey=event.pos;
                mouseClicked=True;
                GAME_SOUND['point'].play();
            
        boxx,boxy=getBoxAtpixel(mousex,mousey);

        if boxx !=None and boxy !=None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx,boxy);
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainbord,[(boxx,boxy)]);
                revealedBoxes[boxx][boxy]=True;


                if firstSelecetion==None:
                    firstSelecetion=(boxx,boxy);
                    

                else:
                    icon1shape,icon1color=getShapeAndColor(mainbord,firstSelecetion[0],firstSelecetion[1]);
                    icon2shape,icon2color=getShapeAndColor(mainbord,boxx,boxy);
                    
                    if icon1shape !=icon2shape or icon1color !=icon2color:
                        GAME_SOUND['hit'].play();
                        pygame.time.wait(1000);
                        coverBoxesAnimation(mainbord,[(firstSelecetion[0],firstSelecetion[1]),(boxx,boxy)]);
                        revealedBoxes[firstSelecetion[0]][firstSelecetion[1]]=False;
                        revealedBoxes[boxx][boxy]=False;
                        

                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainbord);
                        pygame.time.wait(2000);
                        mainbord=getRabdomizedBoed();
                        revealedBoxes=generateReveledBoxesData(False);
                        drawBordr(mainbord,revealedBoxes);
                        pygame.display.update();
                        pygame.time.wait(1000);
                        


                        startGameAnimation(mainbord);
                    firstSelecetion=None;
        pygame.display.update();
        FPSCLOCK.tick(FPS);

def generateReveledBoxesData(val):
    revealedBoxes=[];

    for i in range(BORDERWIDTH):
        revealedBoxes.append([val]*BORDRHEIGHT);
    return revealedBoxes;

def getRabdomizedBoed():
    icons=[];
    for color in ALLCOLOR:
        for shap in ALLSHAPES:
            icons.append((shap,color));
        
    random.shuffle(icons);
    numIconsUsed=int(BORDERWIDTH*BORDRHEIGHT/2);
    icons=icons[:numIconsUsed]*2;
    random.shuffle(icons);
    board=[];
    for x in range(BORDERWIDTH):
        column=[];
        for y in range(BORDRHEIGHT):
            column.append(icons[0]);
            del icons[0];
        board.append(column);
    return board;

def splitIntoGroupOf(groupSize,theList):
    result=[];

    for i in range(0,len(theList),groupSize):
        result.append(theList[i:i+groupSize]);
    return result;

def leftTopCoordOfBox(boxx,boxy):
    left=boxx*(BOXSIZE+GAPSIZE)+XMARGIN;
    top=boxy*(BOXSIZE+GAPSIZE)+YMARGIN;
    return(left,top);

def getBoxAtpixel(x,y):
    for boxx in range(BORDERWIDTH):
        for boxy in range(BORDRHEIGHT):
            left,top=leftTopCoordOfBox(boxx,boxy);
            boxRect=pygame.Rect(left,top,BOXSIZE,BOXSIZE);
            if boxRect.collidepoint(x,y):
                return(boxx,boxy);
    return(None,None);


def drawIcon(shap,color,boxx,boxy):
    quarter=int(BOXSIZE*0.25);
    half=int(BOXSIZE*0.5);


    left,top=leftTopCoordOfBox(boxx,boxy);

    if shap==DOUNT:
        pygame.draw.circle(DISPLAYSURF,color,(left+half,top+half),half-5);
        pygame.draw.circle(DISPLAYSURF,BGCOLOR,(left+half,top+half),quarter-5);

    elif shap==SQUARE:
        pygame.draw.rect(DISPLAYSURF,color,(left+quarter,top+quarter,BOXSIZE-half,BOXSIZE-half))

    elif shap ==DIAMOND:
        pygame.draw.polygon(DISPLAYSURF,color,((left+half,top),(left+BOXSIZE-1,top+half),(left+half,top+BOXSIZE-1),(left,top+half)));


    elif shap==LINSE:
        for i in range(0,BOXSIZE,4):
            pygame.draw.line(DISPLAYSURF,color,(left,top+1),(left+1,top));
            pygame.draw.line(DISPLAYSURF,color,(left+i,top+BOXSIZE-1),(left+BOXSIZE-1,top+1));
    elif shap==OVAL:
        pygame.draw.ellipse(DISPLAYSURF,color,(left,top+quarter,BOXSIZE,half));
        

def getShapeAndColor(board,boxx,boxy):
    return board[boxx][boxy][0],board[boxx][boxy][1];


def drawBoxCovers(board,boxes,coverage):
    for box in boxes:
        left,top=leftTopCoordOfBox(box[0],box[1]);
        pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE,BOXSIZE));

        shap,color=getShapeAndColor(board,box[0],box[1]);
        drawIcon(shap,color,box[0],box[1]);

        if coverage>0:
            pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,coverage,BOXSIZE));
    pygame.display.update();
    FPSCLOCK.tick(FPS);


    
def revealBoxesAnimation(board,boxesToReveal):
    for coverage in range(BOXSIZE,(-REVELASPEED)-1,-REVELASPEED):
        drawBoxCovers(board,boxesToReveal,coverage);
    
def coverBoxesAnimation(board,boxesToCover):
    for coverage in range(0,BOXSIZE+REVELASPEED,REVELASPEED):
        drawBoxCovers(board,boxesToCover,coverage);

def drawBordr(board,revealed):
    for boxx in range(BORDERWIDTH):
        for boxy in range(BORDRHEIGHT):
            left,top=leftTopCoordOfBox(boxx,boxy);
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE,BOXSIZE));
            
            else:
                shap,color=getShapeAndColor(board,boxx,boxy);
                drawIcon(shap,color,boxx,boxy);
            
def drawHighlightBox(boxx,boxy):
    left,top=leftTopCoordOfBox(boxx,boxy);
    pygame.draw.rect(DISPLAYSURF,HIGHLIGHTCOLOR,(left-5,top-5,BOXSIZE+10,BOXSIZE+10),4);

def startGameAnimation(board):
    coveredBoxes=generateReveledBoxesData(False);
    boxes=[];
    for  x in range(BORDERWIDTH):
        for y in range(BORDRHEIGHT):
            boxes.append((x,y));
    random.shuffle(boxes);
    boxGroups=splitIntoGroupOf(8,boxes);

    drawBordr(board,coveredBoxes);
    for boxGroup in boxGroups:
        revealBoxesAnimation(board,boxGroup);
        coverBoxesAnimation(board,boxGroup);

def gameWonAnimation(board):
    coveredBoxes=generateReveledBoxesData(True);
    color1=LIGHTBGCOLOR;
    color2=BGCOLOR;

    for  i in range(13):
        color1,color2=color2,color1;
        DISPLAYSURF.fill(color1);
        drawBordr(board,coveredBoxes);
        pygame.display.update();
        pygame.time.wait(300);
    
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False;
    return True;

if __name__ == "__main__":
    pygame.init();
    FPSCLOCK=pygame.time.Clock();
    
   
    GAME_SOUND['point']=pygame.mixer.Sound('enter the sound for point point.wav');
    
    main();
