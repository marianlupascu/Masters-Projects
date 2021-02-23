package com.main;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import java.io.IOException;
import java.nio.file.Paths;


// From chapter 1

/**
 * This code was originally written for
 * Erik's Lucene intro java.net article
 */
public class Searcher {

    public static void main(String[] args) throws Exception {


        String indexDir = ".\\index";               //1
        if (args.length == 0)
            throw new Exception("Empty query");
        StringBuilder q = new StringBuilder(args[0]);       //2
        //String q = "căruță";

        System.out.println(q);
        search(indexDir, q.toString());
    }

    public static void search(String indexDir, String q)
            throws IOException, ParseException {

        Directory dir = FSDirectory.open(Paths.get(indexDir)); //3
        DirectoryReader directoryReader = DirectoryReader.open(dir);
        IndexSearcher is = new IndexSearcher(directoryReader);   //3

        QueryParser parser = new QueryParser( // 4
                "contents",  //4
                new MyRomanianAnalyzer());  //4
        //parser.setSplitOnWhitespace(true);
        Query query = parser.parse(q);              //4
        System.out.println("query = " + query);
        long start = System.currentTimeMillis();
        TopDocs hits = is.search(query, 1000); //5
        long end = System.currentTimeMillis();

        System.err.println("Found " + hits.totalHits +   //6
                " document(s) (in " + (end - start) +        // 6
                " milliseconds) that matched query '" +     // 6
                q + "':");                                   // 6

        for (ScoreDoc scoreDoc : hits.scoreDocs) {
            Document doc = is.doc(scoreDoc.doc);               //7
            System.out.println(doc.get("originalpath"));  //8
            System.out.println("SCORE = " + scoreDoc.doc);
        }

    }
}

/*
#1 Parse provided index directory
#2 Parse provided query string
#3 Open index
#4 Parse query
#5 Search index
#6 Write search stats
#7 Retrieve matching document
#8 Display filename
*/