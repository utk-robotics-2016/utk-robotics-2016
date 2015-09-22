OBJS := wsServer.o
EXEC := wsServer
CXX := g++
TYPE := cpp
CPPFLAGS := 
CXXFLAGS := -std=c++0x -pthread -g
LDFLAGS := 
LDLIBS := -lwebsockets -lssl -pthread

# link
$(EXEC): $(OBJS)
	$(CXX) $(OBJS) -o $(EXEC) $(LDFLAGS) $(LDLIBS)

# pull in dependency info for *existing* .o files
-include $(OBJS:.o=.d)

# compile and generate dependency info;
# more complicated dependency computation, so all prereqs listed
# will also become command-less, prereq-less targets
#   sed:    strip the target (everything before colon)
#   sed:    remove any continuation backslashes
#   fmt -1: list words one per line
#   sed:    strip leading spaces
#   sed:    add trailing colons
%.o: %.$(TYPE)
	$(CXX) -c $(CPPFLAGS) $(CXXFLAGS) $*.$(TYPE) -o $*.o
	$(CXX) -MM $(CPPFLAGS) $(CXXFLAGS) $*.$(TYPE) > $*.d
	@cp -f $*.d $*.d.tmp
	@sed -e 's/.*://' -e 's/\\$$//' < $*.d.tmp | fmt -1 | \
	sed -e 's/^ *//' -e 's/$$/:/' >> $*.d
	@rm -f $*.d.tmp

# remove compilation products
clean:
	rm -f $(EXEC) *.o *.d
