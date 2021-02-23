package com.main;


import org.apache.lucene.analysis.*;
import org.apache.lucene.analysis.miscellaneous.ASCIIFoldingFilter;
import org.apache.lucene.analysis.miscellaneous.SetKeywordMarkerFilter;
import org.apache.lucene.analysis.ro.RomanianAnalyzer;
import org.apache.lucene.analysis.snowball.SnowballFilter;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.tartarus.snowball.ext.RomanianStemmer;

import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;


public class MyRomanianAnalyzer extends StopwordAnalyzerBase {
    /**
     * File containing default Romanian stopwords.
     */
    public final static String DEFAULT_STOPWORD_FILE = "stopwords.txt";
    /**
     * The comment character in the stopwords file.
     * All lines prefixed with this will be ignored.
     */
    private static final String STOPWORDS_COMMENT = "#";
    private final CharArraySet stemExclusionSet;
    private CharArraySet newStopSet;

    /**
     * Builds an analyzer with the default stop words: {@link #DEFAULT_STOPWORD_FILE}.
     */
    public MyRomanianAnalyzer() {
        this(DefaultSetHolder.DEFAULT_STOP_SET);
        modifyStopWords();
    }

    /**
     * Builds an analyzer with the given stop words.
     *
     * @param stopwords a stopword set
     */
    public MyRomanianAnalyzer(CharArraySet stopwords) {
        this(stopwords, CharArraySet.EMPTY_SET);
        modifyStopWords();
    }

    /**
     * Builds an analyzer with the given stop words. If a non-empty stem exclusion set is
     * provided this analyzer will add a {@link SetKeywordMarkerFilter} before
     * stemming.
     *
     * @param stopwords        a stopword set
     * @param stemExclusionSet a set of terms not to be stemmed
     */
    public MyRomanianAnalyzer(CharArraySet stopwords, CharArraySet stemExclusionSet) {
        super(stopwords);
        this.stemExclusionSet = CharArraySet.unmodifiableSet(CharArraySet.copy(stemExclusionSet));
        modifyStopWords();
    }

    /**
     * Returns an unmodifiable instance of the default stop words set.
     *
     * @return default stop words set.
     */
    public static CharArraySet getDefaultStopSet() {
        return DefaultSetHolder.DEFAULT_STOP_SET;
    }

    /**
     * Creates a
     * {@link org.apache.lucene.analysis.Analyzer.TokenStreamComponents}
     * which tokenizes all the text in the provided {@link Reader}.
     *
     * @return A
     * {@link org.apache.lucene.analysis.Analyzer.TokenStreamComponents}
     * built from an {@link StandardTokenizer} filtered with
     * {@link LowerCaseFilter}, {@link StopFilter}
     * , {@link SetKeywordMarkerFilter} if a stem exclusion set is
     * provided and {@link SnowballFilter}.
     */
    @Override
    protected TokenStreamComponents createComponents(String fieldName) {
        final Tokenizer source = new StandardTokenizer();
        TokenStream result = new LowerCaseFilter(source);
        result = new RemoveDiacriticalsFilter(result);
        result = new StopFilter(result, newStopSet);
        if (!stemExclusionSet.isEmpty())
            result = new SetKeywordMarkerFilter(result, stemExclusionSet);
        result = new SnowballFilter(result, new RomanianStemmer());
        result = new ASCIIFoldingFilter(result);
        return new TokenStreamComponents(source, result);
    }

    private void modifyStopWords() {
        Iterator iter = stopwords.iterator();
        List<String> sw = new ArrayList<>();
        while (iter.hasNext()) {
            char[] stopWord = (char[]) iter.next();
            sw.add(new String(stopWord));

            char[] newStopWord = stopWord.clone();
            for (int i = 0; i < newStopWord.length; i++) {
                if (newStopWord[i] == 'ș' || newStopWord[i] == 'ş')
                    newStopWord[i] = 's';
                if (newStopWord[i] == 'ț' || newStopWord[i] == 'ţ')
                    newStopWord[i] = 't';
                if (newStopWord[i] == 'â')
                    newStopWord[i] = 'a';
                if (newStopWord[i] == 'î')
                    newStopWord[i] = 'i';
                if (newStopWord[i] == 'ă')
                    newStopWord[i] = 'a';
            }
            sw.add(new String(newStopWord));
        }
        sw.add(new String("și"));
        sw.add(new String("si"));

        newStopSet = StopFilter.makeStopSet(sw);
    }

    @Override
    protected TokenStream normalize(String fieldName, TokenStream in) {
        return new LowerCaseFilter(in);
    }

    /**
     * Atomically loads the DEFAULT_STOP_SET in a lazy fashion once the outer class
     * accesses the static final set the first time.;
     */
    private static class DefaultSetHolder {
        static final CharArraySet DEFAULT_STOP_SET;

        static {
            try {
                DEFAULT_STOP_SET = loadStopwordSet(false, RomanianAnalyzer.class,
                        DEFAULT_STOPWORD_FILE, STOPWORDS_COMMENT);
            } catch (IOException ex) {
                // default set should always be present as it is part of the
                // distribution (JAR)
                throw new RuntimeException("Unable to load default stopword set");
            }
        }
    }
}
