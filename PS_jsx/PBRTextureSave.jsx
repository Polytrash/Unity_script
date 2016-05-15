var doc = ""
var docName = "";      // ドキュメント名
var docPath = "C:/a";    // 保存先

uDlg = new Window('dialog','PBRTextureSave',[200,100,510,245]);
uDlg.sText = uDlg.add("statictext",[30,10,275,10+45], "■ _alb   : TGA(RGBA 32Bit) で保存");
uDlg.sText = uDlg.add("statictext",[30,30,275,30+45], "■ _met : TGA(RGBA 32Bit) で保存");
uDlg.sText = uDlg.add("statictext",[30,50,275,50+45], "■ _smo : レイヤーを統合しレイヤーのトップに移動");
var saveBtn = uDlg.add("button",[40,80,275,100+25], "保存", { name:"Save"});


uDlg.show(); 



main();

function main(){
    
            doc= app.activeDocument;
            saveBtn.OnClick = SaveDocToTGA();
    }


function SetupDocBeforeSave(){
       
       var copiedDoc = app.activeDocument.duplicate();    

    }


function getName(){
        
    
    }

function SaveDocToTGA(){       
                
                doc= app.activeDocument;
                docName  = doc.name;
                docPath = doc.path;     
                docName = docName.substring(0, docName.indexOf('.'));
                
                var autoSavePath = docPath + '\\' + docName;
                if ( docName.indexOf('_alb') != -1) {
                                
                    var file = new File(docPath + '\\'  + docName); 
                                
                    tgaOpt = new TargaSaveOptions();
                    tgaOpt.alphaChannels = true;
                    tgaOpt.resolution = TargaBitsPerPixels.THIRTYTWO;
                    tgaOpt.rleCompression = false;                
                
                    doc.saveAs( file, tgaOpt,true, Extension.LOWERCASE);
                }
            
            
                if ( docName.indexOf('_met') != -1) {
                                
                    var file = new File(docPath + '\\'  + docName); 
                                
                    tgaOpt = new TargaSaveOptions();
                    tgaOpt.alphaChannels = true;
                    tgaOpt.resolution = TargaBitsPerPixels.THIRTYTWO;
                    tgaOpt.rleCompression = false;                
                
                    doc.saveAs( file, tgaOpt, true, Extension.LOWERCASE);
                }
            
            
                if (docName.indexOf('_smo') != -1) {
                    
                   var file = new File(docPath + '\\'  + docName); 
                   var copiedDoc = app.activeDocument.duplicate();
                   copiedDoc.mergeVisibleLayers();
                   copiedDoc.selection.selectAll();
                   copiedDoc.selection.copy();
                   copiedDoc.close(SaveOptions.DONOTSAVECHANGES);
                   
                   var dirObj = new File(docPath + '\\' + docName.replace('_smo', '_met'));
                   dirObj.open();
                   
                    var activeChannels = app.activeDocument.channels[2];
                    activeChannels.paste;
                   
                    tgaOpt = new TargaSaveOptions();
                    tgaOpt.alphaChannels = true;
                    tgaOpt.resolution = TargaBitsPerPixels.THIRTYTWO;
                    tgaOpt.rleCompression = false;                
                
                    doc.saveAs( dirObj, tgaOpt, true, Extension.LOWERCASE);                
               }
            

        app.beep();
    
    }
        
 
