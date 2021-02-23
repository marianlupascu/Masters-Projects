package com.main;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.FieldType;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.tika.exception.TikaException;
import org.xml.sax.SAXException;

import java.io.*;
import java.nio.file.Paths;
import java.util.HashMap;

import static com.google.common.io.Files.createTempDir;

// From chapter 1

/**
 * This code was originally written for
 * Erik's Lucene intro java.net article
 */
public class Indexer {

    private static final File myTempDir = createTempDir();
    private static final HashMap<String, String> pathHash = new HashMap<String, String>();
    private final IndexWriter writer;

    public Indexer(String indexDir) throws IOException {
        Directory dir = FSDirectory.open(Paths.get(indexDir));
        writer = new IndexWriter(dir, new IndexWriterConfig(new MyRomanianAnalyzer())); //3
    }

    private static void readData(String file) throws IOException, TikaException, SAXException {
        File folder = new File(file + "\\");
        File[] listOfFiles = folder.listFiles();
        System.out.println(myTempDir.getAbsolutePath());

        assert listOfFiles != null;
        for (File f : listOfFiles) {
            if (f.isFile()) {
                if (f.getName().toLowerCase().endsWith(".txt")) {

                    DocumentReader doc = new DocumentReader();
                    doc.readTXT(f.getAbsolutePath());

                    String txtPath = myTempDir.getAbsolutePath() + "\\" +
                            FilenameUtils.removeExtension(f.getName()) + ".txt";
                    File tempFile = new File(txtPath);
                    FileWriter myWriter = new FileWriter(txtPath);
                    myWriter.write(doc.getContent());
                    myWriter.close();
                    pathHash.put(tempFile.getName(), f.getAbsolutePath());
                }
                if (f.getName().toLowerCase().endsWith(".pdf")) {

                    DocumentReader doc = new DocumentReader();
                    doc.readPDF(f.getAbsolutePath());

                    String txtPath = myTempDir.getAbsolutePath() + "\\" +
                            FilenameUtils.removeExtension(f.getName()) + ".txt";
                    File tempFile = new File(txtPath);
                    FileWriter myWriter = new FileWriter(txtPath);
                    myWriter.write(doc.getContent());
                    myWriter.close();
                    pathHash.put(tempFile.getName(), f.getAbsolutePath());
                }
                if (f.getName().toLowerCase().endsWith(".doc") ||
                        f.getName().toLowerCase().endsWith(".docx")) {

                    DocumentReader doc = new DocumentReader();
                    doc.readDOC(f.getAbsolutePath());

                    String txtPath = myTempDir.getAbsolutePath() + "\\" +
                            FilenameUtils.removeExtension(f.getName()) + ".txt";
                    File tempFile = new File(txtPath);
                    FileWriter myWriter = new FileWriter(txtPath);
                    myWriter.write(doc.getContent());
                    myWriter.close();
                    pathHash.put(tempFile.getName(), f.getAbsolutePath());
                }
            }
        }
    }

    public static void main(String[] args) throws IOException {

        String indexDir = ".\\index";         //1
        String dataDir = ".\\docs";          //2

        if (args.length > 0) {
            dataDir = args[0];          //2
        }

        FileUtils.cleanDirectory(new File(indexDir));

        try {
            PrintStream oldErr = System.err;
            PrintStream newErr = new PrintStream(new ByteArrayOutputStream());
            System.setErr(newErr);

            readData(dataDir);

            System.setErr(oldErr);
        } catch (TikaException | SAXException e) {
            e.printStackTrace();
        }

        Indexer indexer = null;
        long start = System.currentTimeMillis();
        int numIndexed = 0;
        try {
            indexer = new Indexer(indexDir);

            numIndexed = indexer.index(myTempDir.getAbsolutePath(), new TextFilesFilter());
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (indexer != null)
                try {
                    indexer.close();
                } catch (IOException e) {
                    // ignored
                }
        }
        long end = System.currentTimeMillis();

        System.out.println("Indexing " + numIndexed + " files took "
                + (end - start) + " milliseconds");
        myTempDir.deleteOnExit();
    }

    public void close() throws IOException {
        writer.close();                             //4
    }

    public int index(String dataDir, FileFilter filter)
            throws Exception {

        File[] files = new File(dataDir).listFiles();

        assert files != null;
        for (File f : files) {
            if (!f.isDirectory() &&
                    !f.isHidden() &&
                    f.exists() &&
                    f.canRead() &&
                    (filter == null || filter.accept(f))) {
                indexFile(f);
            }
        }

        return writer.numRamDocs();                     //5
    }

    protected Document getDocument(File f) throws Exception {
        Document doc = new Document();
        doc.add(new TextField("contents", new FileReader(f)));      //7
        FieldType notAnalyzed = new FieldType();
        notAnalyzed.setTokenized(true);
        notAnalyzed.setStored(true);
        doc.add(new Field("filename", f.getName(), notAnalyzed));//8
        doc.add(new Field("fullpath", f.getCanonicalPath(), notAnalyzed));//9
        doc.add(new Field("originalpath", pathHash.get(f.getName()), notAnalyzed));
        return doc;
    }

    private void indexFile(File f) throws Exception {
        System.out.println("Indexing " + f.getCanonicalPath());
        Document doc = getDocument(f);
        writer.addDocument(doc);                              //10
    }

    private static class TextFilesFilter implements FileFilter {
        public boolean accept(File path) {
            return path.getName().toLowerCase().endsWith(".txt");  //6
        }
    }
}

/*
#1 Create index in this directory
#2 Index *.txt files from this directory
#3 Create Lucene IndexWriter
#4 Close IndexWriter
#5 Return number of documents indexed
#6 Index .txt files only, using FileFilter
#7 Index file content
#8 Index file name
#9 Index file full path
#10 Add document to Lucene index
*/