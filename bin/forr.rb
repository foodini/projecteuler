require 'find'
require 'pathname'

Find.find(ARGV[0]) do |file|
    file.strip!

    file.gsub!(/\'/, "\\'")
    cmd = "#{ARGV[1]} '#{file}'"
    if Pathname.new(file).file?
	puts cmd
	IO.popen(cmd) do |fd|
	    fd.each_line do |line|
		puts line
	    end
	end
    end
end
