package com.main;

import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;

import java.io.IOException;

public class RemoveDiacriticalsFilter extends TokenFilter {
    private final CharTermAttribute termAtt = this.addAttribute(CharTermAttribute.class);

    public RemoveDiacriticalsFilter(TokenStream in) {
        super(in);
    }

    public final boolean incrementToken() throws IOException {
        if (this.input.incrementToken()) {

            for (int i = 0; i < this.termAtt.buffer().length; i++) {
                if (this.termAtt.buffer()[i] == 'ș' || this.termAtt.buffer()[i] == 'ş')
                    this.termAtt.buffer()[i] = 's';
                if (this.termAtt.buffer()[i] == 'ț' || this.termAtt.buffer()[i] == 'ţ')
                    this.termAtt.buffer()[i] = 't';
                if (this.termAtt.buffer()[i] == 'â')
                    this.termAtt.buffer()[i] = 'a';
                if (this.termAtt.buffer()[i] == 'î')
                    this.termAtt.buffer()[i] = 'i';
                if (this.termAtt.buffer()[i] == 'ă')
                    this.termAtt.buffer()[i] = 'a';
            }
            return true;
        } else {
            return false;
        }
    }
}
