
CPP       = g++
# compiling flags here
FLAGS   = -O2 -Wunused -Wunreachable-code -std=c++98

LINKER   = g++ -o
# linking flags here
LFLAGS   = -Wall -I.

# change these to set the proper directories where each files shoould be
SRCDIR   = src
INCLUDEDIR = include
OBJDIR   = obj
BINDIR   = bin

SOURCES  := $(wildcard $(SRCDIR)/*.c)
INCLUDES := $(wildcard $(INCLUDEDIR)/*.h)

# the objects
OBJECTS  := obj/RNAshapes.o obj/test.o

# executable specific objects

rm       = rm -f

all: $(BINDIR)/test


# compiling
$(OBJECTS): $(OBJDIR)/%.o : $(SRCDIR)/%.cpp
	@$(CPP) $(FLAGS) -c $< -o $@



# linking
$(BINDIR)/test: $(OBJECTS)
	@$(LINKER) $@ $(LFLAGS) $(OBJECTS)



.PHONEY: clean
clean:
	@$(rm) $(OBJECTS)
	@$(rm) $(BINDIR)/*

