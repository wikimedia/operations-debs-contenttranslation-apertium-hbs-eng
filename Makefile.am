###############################################################################
## Makefile for Serbo-Croatian--English
###############################################################################

VERSION=0.5.0
LANG1=hbs
LANG1a=hbs_BS
LANG1b=hbs_HR
LANG1c=hbs_SR
LANG2=eng
VAR1=ijek
VAR2=ek
PREFIX1=$(LANG1)-$(LANG2)
PREFIX2=$(LANG2)-$(LANG1)
PREFIX2a=$(LANG2)-$(LANG1a)
PREFIX2b=$(LANG2)-$(LANG1b)
PREFIX2c=$(LANG2)-$(LANG1c)

BASENAME=apertium-$(PREFIX1)

TARGETS_COMMON = \
	Cyrl-Latn.autopmor.bin \
	$(PREFIX1).autobil.bin \
	$(PREFIX1).autogen.bin \
	$(PREFIX1).autolex.bin \
	$(PREFIX1).automorf.bin \
	$(PREFIX1).autopgen.bin \
	$(PREFIX1).rlx.bin \
	$(PREFIX1).t1x.bin \
	$(PREFIX1).t2x.bin \
	$(PREFIX1).t3x.bin \
	$(PREFIX2a).autogen.bin \
	$(PREFIX2a).autolex.bin \
	$(PREFIX2a).autopgen.bin \
	$(PREFIX2).autobil.bin \
	$(PREFIX2).automorf.bin \
	$(PREFIX2b).autogen.bin \
	$(PREFIX2b).autolex.bin \
	$(PREFIX2b).autopgen.bin \
	$(PREFIX2c).autogen.bin \
	$(PREFIX2c).autolex.bin \
	$(PREFIX2c).autopgen.bin \
	$(PREFIX2).rlx.bin \
	$(PREFIX2).t1x.bin \
	$(PREFIX2).t2x.bin \
	$(PREFIX2).t3x.bin


# This include defines goals for install-modes, .deps/.d and .mode files:
@ap_include@

###############################################################################
## Transducers, disambiguation rules, transfer
###############################################################################


$(PREFIX2a).autogen.bin: $(AP_SRC1)/$(LANG1a).autogen.bin
	cp $< $@

$(PREFIX2b).autogen.bin: $(AP_SRC1)/$(LANG1b).autogen.bin
	cp $< $@

$(PREFIX2c).autogen.bin: $(AP_SRC1)/$(LANG1c).autogen.bin
	cp $< $@


$(PREFIX2a).autolex.bin: $(BASENAME).$(PREFIX2a).lrx
	lrx-comp $(BASENAME).$(PREFIX2a).lrx $@

$(PREFIX2b).autolex.bin: $(BASENAME).$(PREFIX2b).lrx
	lrx-comp $(BASENAME).$(PREFIX2b).lrx $@

$(PREFIX2c).autolex.bin: $(BASENAME).$(PREFIX2c).lrx
	lrx-comp $(BASENAME).$(PREFIX2c).lrx $@


Cyrl-Latn.autopmor.bin: $(AP_SRC1)/apertium-$(LANG1).Cyrl-Latn.dix
	apertium-validate-dictionary $(AP_SRC1)/apertium-$(LANG1).Cyrl-Latn.dix
	lt-comp lr $^ $@


$(PREFIX1).automorf.bin: $(AP_SRC1)/$(LANG1).automorf.bin $(PREFIX1).autobil.bin
	lt-trim $< $(PREFIX1).autobil.bin $@

$(PREFIX1).autogen.bin: $(BASENAME).$(LANG2).dix
	apertium-validate-dictionary $(BASENAME).$(LANG2).dix
	lt-comp rl $(BASENAME).$(LANG2).dix $@

$(PREFIX1).rlx.bin: $(AP_SRC1)/$(LANG1).rlx.bin
	cp $< $@

$(PREFIX2).rlx.bin: $(BASENAME).$(PREFIX2).rlx
	cg-comp $(BASENAME).$(PREFIX2).rlx $@

$(PREFIX1).autolex.bin: $(BASENAME).$(PREFIX1).lrx
	lrx-comp $(BASENAME).$(PREFIX1).lrx $@

$(PREFIX2a).autopgen.bin: $(AP_SRC1)/$(LANG1c).autopgen.bin
	cp $< $@

$(PREFIX2b).autopgen.bin: $(AP_SRC1)/$(LANG1c).autopgen.bin
	cp $< $@

$(PREFIX2c).autopgen.bin: $(AP_SRC1)/$(LANG1c).autopgen.bin
	cp $< $@

$(PREFIX2).automorf.bin: $(BASENAME).$(LANG2).dix
	apertium-validate-dictionary $(BASENAME).$(LANG2).dix
	lt-comp lr $(BASENAME).$(LANG2).dix $@ $(BASENAME).$(LANG2).acx

$(PREFIX1).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $(BASENAME).$(PREFIX1).dix
	lt-comp lr $(BASENAME).$(PREFIX1).dix $@


$(PREFIX2).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $(BASENAME).$(PREFIX1).dix
	lt-comp rl $(BASENAME).$(PREFIX1).dix $@

$(PREFIX1).autopgen.bin: $(BASENAME).post-$(LANG2).dix
	apertium-validate-dictionary $(BASENAME).post-$(LANG2).dix
	lt-comp lr $(BASENAME).post-$(LANG2).dix $@

#
#	TRANSFER
#

$(PREFIX1).t1x.bin: $(BASENAME).$(PREFIX1).t1x
	apertium-validate-transfer $(BASENAME).$(PREFIX1).t1x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t1x $@

$(PREFIX1).t2x.bin: $(BASENAME).$(PREFIX1).t2x
	apertium-validate-interchunk $(BASENAME).$(PREFIX1).t2x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t2x $@

$(PREFIX1).t3x.bin: $(BASENAME).$(PREFIX1).t3x
	apertium-validate-postchunk $(BASENAME).$(PREFIX1).t3x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX1).t3x $@

$(PREFIX2).t1x.bin: $(BASENAME).$(PREFIX2).t1x
	apertium-validate-transfer $(BASENAME).$(PREFIX2).t1x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t1x $@

$(PREFIX2).t2x.bin: $(BASENAME).$(PREFIX2).t2x
	apertium-validate-interchunk $(BASENAME).$(PREFIX2).t2x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t2x $@

$(PREFIX2).t3x.bin: $(BASENAME).$(PREFIX2).t3x
	apertium-validate-postchunk $(BASENAME).$(PREFIX2).t3x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t3x $@


###############################################################################
## Distribution
###############################################################################

EXTRA_DIST=$(BASENAME).$(PREFIX1).dix \
           $(BASENAME).$(LANG2).dix \
           $(BASENAME).$(LANG2).acx \
           $(BASENAME).post-$(LANG2).dix \
           $(PREFIX1).prob $(PREFIX2).prob \
           $(BASENAME).$(PREFIX1).lrx $(BASENAME).$(PREFIX2a).lrx $(BASENAME).$(PREFIX2b).lrx $(BASENAME).$(PREFIX2c).lrx \
           $(BASENAME).$(PREFIX2).rlx \
           $(BASENAME).$(PREFIX1).t1x $(BASENAME).$(PREFIX1).t2x \
           $(BASENAME).$(PREFIX1).t3x $(BASENAME).$(PREFIX2).t1x \
           $(BASENAME).$(PREFIX2).t2x $(BASENAME).$(PREFIX2).t3x \
           modes.xml


###############################################################################
## Installation
###############################################################################

apertium_hbs_engdir=$(prefix)/share/apertium/$(BASENAME)/

# Files which should be installed to $(prefix)/share/apertium/$(BASENAME)/:
apertium_hbs_eng_DATA=$(TARGETS_COMMON) \
	$(PREFIX1).prob $(PREFIX2).prob \
	$(BASENAME).$(PREFIX1).t1x \
	$(BASENAME).$(PREFIX1).t2x \
	$(BASENAME).$(PREFIX1).t3x \
	$(BASENAME).$(PREFIX2).t1x \
	$(BASENAME).$(PREFIX2).t2x \
	$(BASENAME).$(PREFIX2).t3x


# All modes are created by the same goal, listing several will just give problems with make -j2
noinst_DATA=modes/$(PREFIX1).mode

install-data-local: install-modes


###############################################################################
## Cleanup
###############################################################################

CLEANFILES = $(TARGETS_COMMON)
clean-local: 
	-rm -rf .deps modes
