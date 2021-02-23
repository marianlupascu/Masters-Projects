package com.main;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.microsoft.ooxml.OOXMLParser;
import org.apache.tika.parser.pdf.PDFParser;
import org.apache.tika.parser.txt.TXTParser;
import org.apache.tika.sax.BodyContentHandler;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;

public class DocumentReader {
    private BodyContentHandler handler;
    private Metadata metadata;
    private FileInputStream inputstream;
    private ParseContext pcontext;

    private void read(String pathname) throws FileNotFoundException {
        //detecting the file type
        handler = new BodyContentHandler(-1);
        metadata = new Metadata();
        inputstream = new FileInputStream(new File(pathname));
        pcontext = new ParseContext();
    }

    public void readPDF(String pathname) throws IOException, TikaException, SAXException {

        read(pathname);
        //parsing the document using PDF parser
        PDFParser pdfparser = new PDFParser();
        pdfparser.parse(inputstream, handler, metadata, pcontext);
    }

    public void readTXT(String pathname) throws IOException, TikaException, SAXException {
        read(pathname);

        //Text document parser
        TXTParser TexTParser = new TXTParser();
        TexTParser.parse(inputstream, handler, metadata, pcontext);
    }

    public void readDOC(String pathname) throws IOException, TikaException, SAXException {
        read(pathname);

        //OOXml parser
        OOXMLParser msofficeparser = new OOXMLParser();
        msofficeparser.parse(inputstream, handler, metadata, pcontext);
    }

    public String getContent() {
        return handler.toString();
    }

    public void showMetadata() {
        //getting metadata of the document
        System.out.println("Metadata of the doc:");
        String[] metadataNames = metadata.names();

        for (String name : metadataNames) {
            System.out.println(name + " : " + metadata.get(name));
        }
    }

    public void print() {
        //getting the content of the document
        System.out.println("Contents of the doc :" + handler.toString());

        showMetadata();
    }
}
